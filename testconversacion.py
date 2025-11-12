#/raiz/tesconversacion.py
#Script para probar un flujo de conversación controlado, usando tu ConversationState y generate.
#simulando un mensaje del usuario.
from core.conversation import ConversationState
from core.prompting import build_messages
from services.llm import generate

def test_conversation():
    # Crear instancia de ConversationState
    conversation_state = ConversationState()

    # Mensaje inicial del usuario
    user_input = "Hola, ¿cómo estás?"

    # Simular la respuesta del asistente (debe ser generada por el modelo real)
    assistant_response = "¡Hola! Estoy bien, gracias por preguntar. ¿En qué te puedo ayudar?"

    # Actualizar el historial de la conversación
    conversation_state.update_state(user_input, assistant_response)

    # Preparar los mensajes para el modelo
    messages = build_messages(conversation_state.history, "Assistant", max_turns=3)

    # Generar la siguiente respuesta utilizando el modelo de Hugging Face
    response = generate(messages)

    # Mostrar la respuesta generada por el modelo
    print("Respuesta generada:", response)

# Ejecutar la prueba
if __name__ == "__main__":
    test_conversation()
