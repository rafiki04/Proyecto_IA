# /core/conversation.py
from typing import List, Dict
from services import llm

MAX_HISTORY = 20  # 20 turnos ≈ 40 mensajes (user+assistant)

def init_state() -> Dict[str, List[Dict[str, str]]]:
    """Inicializa el estado de la conversación."""
    return {"history": [], "intents": []}

class ConversationState:
    """Estado de la conversación: historial, intents y truncado."""

    def __init__(self):
        self.intents: List[str] = []
        self.history: List[Dict[str, str]] = []

    def update_state(self, user_input: str, assistant_response: str = None):
        """Actualiza historial, detecta intents y genera respuesta por defecto."""
        
        # Detectar intents locales
        if user_input.startswith("/"):
            intent = user_input.split()[0]
            self.intents.append(intent)

            if intent == "/nota":
                content = user_input[len("/nota"):].strip()
                assistant_response = f"Nota guardada: '{content}'"
            elif intent == "/recordatorio":
                content = user_input[len("/recordatorio"):].strip()
                assistant_response = f"Recordatorio agregado: '{content}'"
            elif intent == "/busqueda":
                query = user_input[len("/busqueda"):].strip()
                assistant_response = f"Resultado de búsqueda para '{query}': (simulado)"
            else:
                assistant_response = "Intent no reconocido."

        # Si no pasa assistant_response, genera placeholder
        if assistant_response is None:
            assistant_response = "…"

        # Guarda en historial
        self.history.append({"role": "user", "content": user_input})
        self.history.append({"role": "assistant", "content": assistant_response})

        # Trunca a los últimos MAX_HISTORY turnos
        if len(self.history) > MAX_HISTORY * 2:
            self.history = self.history[-MAX_HISTORY*2:]
            self.history[-1] = {
              "role": "assistant",
                "content": f"Has alcanzado el límite de turnos ({MAX_HISTORY}). La sesión se reiniciará en el próximo mensaje."
            }

    def get_recent_history(self, turns: int = 5) -> List[Dict[str, str]]:
        """Devuelve las últimas interacciones para construir prompt."""
        return self.history[-turns*2:]  # cada turno = user+assistant

def ask(state: Dict[str, List[Dict[str, str]]], user_input: str) -> str:
    assistant_response = None
    insecure_keywords = ["delete", "elimina", "borra", "haz algo ilegal"]

    # Se detecta inputs inseguros primero
    if any(word in user_input.lower() for word in insecure_keywords):
        assistant_response = "Lo siento, no puedo realizar esa acción."

    # Detecta intents válidos
    elif user_input.startswith("/"):
        intent = user_input.split()[0]
        if "intents" not in state:
            state["intents"] = []
        state["intents"].append(intent)

        if intent == "/nota":
            assistant_response = f" Nota guardada: '{user_input[len('/nota'):].strip()}'"
        elif intent == "/recordatorio":
            assistant_response = f" Recordatorio agregado: '{user_input[len('/recordatorio'):].strip()}'"
        elif intent == "/busqueda":
            assistant_response = f" Resultado de búsqueda para '{user_input[len('/busqueda'):].strip()}': (simulado)"
        else:
            assistant_response = "Intent no reconocido."

    # Si no hay respuesta, llamamos al LLM
    if assistant_response is None:
        try:
            messages = state.get("history", []) + [{"role": "user", "content": user_input}]
            assistant_response = llm.generate(messages)
            if not assistant_response:
                raise ValueError("Respuesta vacía del modelo.")
        except Exception as e:
            assistant_response = f"Ocurrió un error al generar la respuesta: {e}"

    # 4Guardar en historial
    conv_state = ConversationState()
    conv_state.history = state.get("history", [])
    conv_state.update_state(user_input, assistant_response)
    state["history"] = conv_state.history

    return assistant_response
