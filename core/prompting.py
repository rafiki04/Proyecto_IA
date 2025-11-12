# /raiz/core/prompting.py
from typing import List, Dict

SYSTEM_PROMPT = "Eres AI Copilot, un asistente digital que ayuda con tareas, búsqueda y educación."

def build_messages(history: List[Dict[str, str]], user_input: str, max_turns: int = 5) -> List[Dict[str, str]]:
    """
    Construye la lista de mensajes para enviar al LLM.
    Mantiene los últimos `max_turns` turnos y agrega el system prompt.
    """
    truncated_history = history[-max_turns:]
    messages = [{"role": "system", "content": SYSTEM_PROMPT}] + truncated_history
    messages.append({"role": "user", "content": user_input})
    return messages
