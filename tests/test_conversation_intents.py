import pytest
from core.conversation import ConversationState

@pytest.fixture
def conv():
    return ConversationState()

def test_intent_nota(conv):
    user_input = "/nota Comprar leche"
    assistant_response = ""
    conv.update_state(user_input, assistant_response)

    last_assistant = conv.history[-1]["content"]
    last_user = conv.history[-2]["content"]

    assert last_user == user_input
    assert "Nota guardada" in last_assistant
    assert conv.intents[-1] == "/nota"

def test_intent_recordatorio(conv):
    user_input = "/recordatorio Llamar a Juan a las 5pm"
    assistant_response = ""
    conv.update_state(user_input, assistant_response)

    last_assistant = conv.history[-1]["content"]
    last_user = conv.history[-2]["content"]

    assert last_user == user_input
    assert "Recordatorio agregado" in last_assistant
    assert conv.intents[-1] == "/recordatorio"

def test_intent_busqueda(conv):
    user_input = "/busqueda Clima hoy en CDMX"
    assistant_response = ""
    conv.update_state(user_input, assistant_response)

    last_assistant = conv.history[-1]["content"]
    last_user = conv.history[-2]["content"]

    assert last_user == user_input
    assert "Resultado de búsqueda" in last_assistant
    assert conv.intents[-1] == "/busqueda"

def test_truncado_historial(conv):
    """
    Simula muchos turnos (> MAX_HISTORY) para asegurar truncado correcto.
    """
    MAX_HISTORY = 20  
    
    for i in range(25):
        conv.update_state(f"/nota Turno {i}", "")

    # Historial completo tiene usuario + assistant => 25*2=50 mensajes
    # Pero truncado a MAX_HISTORY => 20 turnos = 40 mensajes
    assert len(conv.history) <= MAX_HISTORY * 2
    # Verifica que los turnos más recientes estén presentes
    assert "Turno 24" in conv.history[-2]["content"]
    assert len(conv.history) <= MAX_HISTORY * 2

# Validamos que los turnos más recientes estén presentes
    assert "Turno 24" in conv.history[-2]["content"]  # último turno usuario
    assert "Has alcanzado el límite de turnos" in conv.history[-1]["content"]
    #assert "Turno 24" in conv.history[-1]["content"]   último turno assistant
    


