#raiz/pruebachat.py
#Es un mini demo manual de chat sin interfaz web ni tests
#run.py: Usa la lógica de ask() directamente, no ConversationManager ni LLMClient. Es más simple.
from core import conversation

state = conversation.init_state()

print("Chat con tu modelo (escribe 'salir' para terminar)\n")
while True:
    user_input = input("Tú: ")
    if user_input.lower() in ["salir", "exit", "quit"]:
        break
    reply = conversation.ask(state, user_input)
    print(" Asistente:", reply)
