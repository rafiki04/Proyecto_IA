#genera panorama de las metricas acumuladas  y mostrarlas en consola.

# raiz/tests/testmetricas
from services.llm import generate, mostrar_metricas

messages = [
    {"role": "system", "content": "Eres AI Copilot, un asistente útil y educado."},
    {"role": "user", "content": "Hola, ¿puedes presentarte?"}
]

response = generate(messages)
print("\nRespuesta del modelo:\n", response)

# Mostrar métricas acumuladas
mostrar_metricas()
