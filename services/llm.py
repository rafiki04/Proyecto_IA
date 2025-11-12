# raiz/services/llm.py
import os
import time
import statistics
import logging
import uuid
from typing import List, Dict, Optional
from dotenv import load_dotenv

# Import del cliente HugginFace si esta instalado en el entorno
try:
    from huggingface_hub import InferenceClient
except Exception:
    InferenceClient = None

# Variable global para usar modo simulado cuando se acaben los créditos
USE_SIMULATED = False  # si es True, genera respuestas simuladas sin usar HF

# Cargar .env (usar la ruta relativa o donde se encuentre)
load_dotenv()
HF_API_TOKEN = os.getenv("HF_API_TOKEN")
MODEL_ID = os.getenv("MODEL_ID")
MAX_TOKENS = int(os.getenv("MAX_TOKENS", 512))
TEMPERATURE = float(os.getenv("TEMPERATURE", 0.7))
TOP_P = float(os.getenv("TOP_P", 0.9))
RETRIES = int(os.getenv("RETRIES", 2))
TIMEOUT = int(os.getenv("LLM_TIMEOUT", 12))
print("[DEBUG] .env cargado desde:", os.getcwd())
print("[DEBUG] HF_API_TOKEN:", HF_API_TOKEN)
print("[DEBUG] MODEL_ID:", MODEL_ID)

# Inicializa cliente HF solo si token y client se encuentran disponibles
client = None
if InferenceClient is not None and HF_API_TOKEN:
    try:
        client = InferenceClient(token=HF_API_TOKEN)
    except Exception as e:
        client = None

# Logging
logging.basicConfig(
    filename="logs_llm.txt",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

LATENCIAS: List[float] = []
REINTENTOS = 0
FALLBACKS = 0

def _extract_text_from_result(result) -> str:
    if result is None:
        return ""
    if isinstance(result, str):
        return result.strip()
    if isinstance(result, dict):
        for key in ("generated_text", "text", "output", "content"):
            val = result.get(key)
            if isinstance(val, str) and val.strip():
                return val.strip()
        for val in result.values():
            if isinstance(val, str) and val.strip():
                return val.strip()
            if isinstance(val, list) and val and isinstance(val[0], str):
                return val[0].strip()
    if isinstance(result, list):
        first = result[0]
        if isinstance(first, dict):
            for key in ("generated_text", "text", "content"):
                val = first.get(key)
                if isinstance(val, str) and val.strip():
                    return val.strip()
        elif isinstance(first, str):
            return first.strip()
    return str(result).strip()


def generate(messages: List[Dict[str, str]],
             simulate_error: Optional[int] = None,
             request_id: Optional[str] = None) -> str:
    """
    Genera la respuesta llamando al LLM.
    Si se acaban los créditos o USE_SIMULATED=True, usa fallback local.
    """
    global REINTENTOS, FALLBACKS, USE_SIMULATED

    if request_id is None:
        request_id = str(uuid.uuid4())

    prompt = "\n".join([f"{m['role']}: {m['content']}" for m in messages])

    # Simulación de error para tests
    if simulate_error is not None:
        raise Exception(f"Simulated error {simulate_error}")

    for attempt in range(RETRIES + 1):
        start_time = time.time()
        try:
            if client is None or USE_SIMULATED:
                # fallback local
                result_raw = f"Simulated model response for prompt (len={len(prompt)})"
            else:
                # Llamada real al cliente HuggingFace
                if "Instruct" in MODEL_ID or "Llama-3" in MODEL_ID:
                    result_raw = client.chat.completions.create(
                        model=MODEL_ID,
                        messages=[
                            {"role": "system", "content": "Eres un asistente útil que responde en español."},
                            {"role": "user", "content": prompt},
                        ],
                        max_tokens=MAX_TOKENS,
                        temperature=TEMPERATURE,
                        top_p=TOP_P,
                    )
                    result_raw = result_raw.choices[0].message["content"]
                else:
                    result_raw = client.text_generation(
                        model=MODEL_ID,
                        prompt=prompt,
                        max_new_tokens=MAX_TOKENS,
                        temperature=TEMPERATURE,
                        top_p=TOP_P,
                        stop=["user:", "system:"],
                    )

            latency = time.time() - start_time
            LATENCIAS.append(latency)

            text = _extract_text_from_result(result_raw)
            input_tokens = len(prompt.split())
            output_tokens = len(text.split())
            total_tokens = input_tokens + output_tokens

            logging.info(f"{request_id} | OK | attempt={attempt+1} | latencia={latency:.2f}s | tokens≈{total_tokens}")
            print(f"Respuesta exitosa | request_id={request_id} | latencia={latency:.2f}s | tokens≈{total_tokens}")
            return text.strip()

        except Exception as e:
            REINTENTOS += 1
            latency = time.time() - start_time
            error_str = str(e)

            # Detecta error en créditos y activa el modo simulado
            if "402 Client Error" in error_str:
                USE_SIMULATED = True
                print("Créditos agotados: usando modo simulado para tests.")
                result_raw = f"Simulated model response for prompt (len={len(prompt)})"
                return result_raw

            # Logging normal de errores
            if "401" in error_str or "403" in error_str or "404" in error_str:
                error_type = "4xx (cliente)"
            elif "500" in error_str or "502" in error_str or "503" in error_str:
                error_type = "5xx (servidor)"
            else:
                error_type = "otro"

            logging.warning(f"{request_id} | ERROR {error_type} | attempt={attempt+1} | detalle={e} | latencia={latency:.2f}s")
            print(f"Error {error_type} | request_id={request_id} | intento {attempt+1}: {e}")

            if attempt < RETRIES:
                backoff = 2 ** attempt
                time.sleep(backoff)
                continue
            else:
                FALLBACKS += 1
                fallback_msg = f"Lo siento, no puedo procesar tu solicitud en este momento. (request_id={request_id})"
                logging.error(f"{request_id} | Fallback activado tras agotar reintentos.")
                print(f"Fallback activado | request_id={request_id}")
                return fallback_msg


def mostrar_metricas():
    if LATENCIAS:
        p50 = statistics.median(LATENCIAS)
        sorted_lat = sorted(LATENCIAS)
        idx95 = max(0, int(0.95 * len(sorted_lat)) - 1)
        p95 = sorted_lat[idx95]
    else:
        p50 = p95 = 0.0

    print("\nMÉTRICAS DEL MODELO")
    print(f"• Latencia p50: {p50:.2f}s")
    print(f"• Latencia p95: {p95:.2f}s")
    print(f"• Reintentos totales: {REINTENTOS}")
    print(f"• Fallbacks activados: {FALLBACKS}")
    print(f"• Total de llamadas exitosas: {len(LATENCIAS)}")

    logging.info(f"MÉTRICAS | p50={p50:.2f}s | p95={p95:.2f} | reintentos={REINTENTOS} | fallbacks={FALLBACKS}")
