#verificacion del token de HuggingFace. Solo para confirmar que el token y el modelo funciona.

#raiz/tests/nuevotest

from huggingface_hub import InferenceClient, whoami
from dotenv import load_dotenv
import os

# Carga las variables de entorno (.env la carpeta del proyecto)
load_dotenv("C:/Users/cris_/Downloads/ProyectoIA/.env")

# Se imprime para confirmar que sí se cargan
print("TOKEN:", os.getenv("HF_API_TOKEN"))
print("MODEL:", os.getenv("MODEL_ID"))

# Se verifica el token con Hugging Face
try:
    user_info = whoami(token=os.getenv("HF_API_TOKEN"))
    print("Token válido. Usuario conectado:", user_info.get("name"))
except Exception as e:
    print("Error verificando token:", e)
    exit()

# Esto crea cliente de inferencia
client = InferenceClient(
    model=os.getenv("MODEL_ID"),
    token=os.getenv("HF_API_TOKEN")
)

# Prueba de inferencia
try:
    print("\nProbando inferencia...")
    result = client.text_generation(
        prompt="Hola, ¿puedes presentarte brevemente?",
        max_new_tokens=50,
        temperature=0.7,
        top_p=0.9
    )
    print("\n✅Respuesta del modelo:\n")
    print(result)
except Exception as e:
    print("\n❌ Error en inferencia:", e)
