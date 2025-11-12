# run.py modificado
from core.conversation import ConversationState, ask, init_state

state = init_state()
conv_state = ConversationState()
state["history"] = conv_state.history

print(" AI Copilot listo. Usa /nota, /recordatorio, /busqueda o escribe 'salir'.\n")

while True:
    user_input = input("Tú: ")
    if user_input.lower() in ["salir", "exit", "quit"]:
        break

    reply = ask(state, user_input)
    print("AI Copilot:", reply)
