# tests/test_prompting.py
from core.prompting import build_messages

def test_build_messages_truncation():
    # Creamos 10 mensajes de ejemplo
    history = [{"role": "user", "content": f"msg{i}"} for i in range(10)]
    
    # Usamos build_messages con un límite de 3 turnos (máximo de 3 turnos + system prompt)
    msgs = build_messages(history, "nuevo", max_turns=3)

    # El mensaje final debe incluir los 3 últimos mensajes del usuario + el system prompt
    assert len(msgs) == 5  # 3 turnos de usuario + 1 mensaje system prompt + 1 del último turno de usuario
