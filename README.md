# AI Copilot - Chatbot MVP

## 1. Descripción

AI Copilot es un asistente digital mínimo viable (MVP) diseñado para demostrar cómo un LLM puede asistir a los usuarios en:

- **Tareas diarias:** notas, recordatorios y agenda.
- **Búsqueda rápida:** respuestas tipo buscador.
- **Educación y productividad:** tips, guías y apoyo contextual.

El sistema implementa:

- **Integración robusta con un LLM** (`Meta-Llama-3-8B-Instruct` vía Hugging Face).
- **Conversación contextual** limitada a 20 turnos (usuario + asistente).
- **Detección de intents simples:** `/nota`, `/recordatorio`, `/busqueda`.
- **Manejo de errores y fallback visible** ante problemas del LLM.
- **Simulación offline** de respuestas si falla el modelo real o se agotan créditos.

---

## 2. Objetivo del proyecto

El propósito es evaluar la capacidad de integrar un LLM de forma robusta, controlando:

- Parámetros de inferencia (`temperature`, `top_p`, `max_tokens`, `seed`)
- Truncado de historial y memoria corta
- Reintentos y backoff ante errores 4xx/5xx
- Fallback claro y trazable
- Lógica de conversación coherente con intents simples

No se evalúa estética o complejidad visual, sino **funcionalidad y robustez del MVP**.

---

## 3. Stack técnico y modelo utilizado

- **Lenguaje:** Python 3.13  
- **Framework web:** Gradio  
- **Modelo LLM:** `meta-llama/Meta-Llama-3-8B-Instruct`  
- **Proveedor:** Hugging Face  
- **Justificación:** Modelo instructivo, adecuado para generación de texto conversacional y soporte a intents simples.

---

## 4. Parámetros de inferencia

- `temperature`: 0.7  
- `top_p`: 0.9  
- `max_tokens`: 512  
- `seed`: aleatorio por defecto  
- **Rationale:** Balance entre creatividad y coherencia, evitando respuestas demasiado aleatorias.

---

## 5. Lógica de la conversación

- Conversación limitada a 20 turnos (usuario + asistente).  
- Los prompts se construyen usando `build_messages()` en cada interacción.  
- El estado de la conversación se mantiene con `ConversationState` y se actualiza con `update_state()`.  
- Si el modelo falla, se muestra un **fallback visible** (“Lo siento, no puedo…”).  
- Se soportan intents básicos para notas, recordatorios y búsquedas.

---

## 6. Métricas de desempeño

Resultados medidos en pruebas reales:

| Métrica                  | Valor           |
|---------------------------|----------------|
| Latencia p50              | 2.24–3.81 s    |
| Latencia p95              | 3.81 s         |
| Reintentos totales        | 0              |
| Fallbacks activados       | 0              |
| Total de llamadas exitosas| 5              |
| Tokens promedio por respuesta | 292 aprox. |

> Latencias calculadas a partir de ejecuciones de `llm.generate()` con 5 preguntas de prueba.

---

## 7. Limitaciones

- Historial limitado a 20 turnos y no persistente entre sesiones.  
- Modelo no recuerda preferencias personales más allá del contexto temporal.  


## 8. Estructura del proyecto
/core
--conversation.py # Manejo del estado de la conversación, intents y truncado
--prompting.py # Construcción de prompts y truncado de historial
/services
--llm.py # Cliente LLM con retries, fallback y métricas
/app
--web.py # Interfaz web Gradio para el chat
/tests
--test_llm_retry_fallback.py # Reintentos y fallback del LLM
--test_insecure_requests.py # Inputs inseguros
--test_e2e_ana.py # Flujo E2E de conversación
--test_llm_1.py # Prueba básica de generación
--test_llm_fallback.py # Prueba de fallback
--test_prompting.py # Truncado y construcción de mensajes
--testchatbot.py # Test informal de conversación completa
--conftest.py # Configuración de pytest y modo simulado
README.md # Documentación completa
requirements.txt # Dependencias Python
logs_llm.txt # Logs de métricas
