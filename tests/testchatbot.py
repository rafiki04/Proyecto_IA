#test informal para mostrar en pantalla la conversacion en panatalla simualada.


#raiz/tests/testchatbot
from core.conversation import ConversationState
from core.prompting import build_messages
from services.llm import generate

print("Iniciando prueba completa de AI Copilot...\n")

conv = ConversationState()

# Simulamos una conversación
user_inputs = [
    "Hola, ¿puedes presentarte?",
    "Mi nombre es Ana.",
    "¿Puedes recordarme cómo me llamo?",
    "¿Qué puedes hacer por mí?",
    "Dame un tip rápido de productividad.",
]

for user_input in user_inputs:
    print(f" Usuario: {user_input}")
    messages = build_messages(conv.get_recent_history(), user_input)
    response = generate(messages)
    conv.update_state(user_input, response)
    print(f"AI Copilot: {response}\n")

print("Conversación completa probada correctamente.")
