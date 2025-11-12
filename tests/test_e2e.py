#/tests/test_e2e.py
import uuid
import pytest
from core import conversation
from services import llm

def test_conversacion_basica(monkeypatch):
    state = conversation.init_state()
    # Simulamos dos mensajes básicos
    r1 = conversation.ask(state, "Me llamo Ana")
    assert isinstance(r1, str)
    r2 = conversation.ask(state, "¿Cómo me llamo?")
    #assert "ana" in r2.lower()
    if llm.USE_SIMULATED:
        assert isinstance(r2, str)
    else:
        assert "ana" in r2.lower()

@pytest.mark.parametrize("use_real", [False])
def test_fallback_clave_invalida(monkeypatch, use_real):
    # Guardamos la función original ANTES de reemplazarla
    original_generate = llm.generate

    def mock_generate_error(*args, **kwargs):
        return original_generate(args[0], simulate_error=401, request_id=str(uuid.uuid4()))

    # Reemplazamos la función en llm
    monkeypatch.setattr(llm, "generate", mock_generate_error)

    state = conversation.init_state()
    response = conversation.ask(state, "Hola")
    assert "error" in response.lower() or "token" in response.lower()
def test_contexto_tras_varios_turnos():
    """
    Verifica que el chatbot mantenga coherencia después de varios turnos.
    Si el contexto se trunca (por límite de historial), la respuesta debe
    seguir siendo razonable (como "no recuerdo", etc.).
    """
    state = conversation.init_state()
    conversation.ask(state, "Mi color favorito es azul")
    
    # Simulamos varios turnos (8 mensajes más)
    for i in range(8):
        conversation.ask(state, f"Turno {i+1}")
    
#/tests/test_e2e.py
import uuid
import pytest
from core import conversation
from services import llm

def test_conversacion_basica(monkeypatch):
    state = conversation.init_state()
    # Simulamos dos mensajes básicos
    r1 = conversation.ask(state, "Me llamo Ana")
    assert isinstance(r1, str)
    r2 = conversation.ask(state, "¿Cómo me llamo?")
    #assert "ana" in r2.lower()
    if llm.USE_SIMULATED:
        assert isinstance(r2, str)
    else:
        assert "ana" in r2.lower()

@pytest.mark.parametrize("use_real", [False])
def test_fallback_clave_invalida(monkeypatch, use_real):

    original_generate = llm.generate

    def mock_generate_error(*args, **kwargs):
        return original_generate(args[0], simulate_error=401, request_id=str(uuid.uuid4()))

    
    monkeypatch.setattr(llm, "generate", mock_generate_error)

    state = conversation.init_state()
    response = conversation.ask(state, "Hola")
    assert "error" in response.lower() or "token" in response.lower()
def test_contexto_tras_varios_turnos():
    """
    Verifica que el chatbot mantenga coherencia después de varios turnos.
    Si el contexto se trunca (por límite de historial), la respuesta debe
    seguir siendo razonable ("no recuerdo", etc.).
    """
    state = conversation.init_state()
    conversation.ask(state, "Mi color favorito es azul")
    
    # Simulamos varios turnos (8 mensajes más)
    for i in range(8):
        conversation.ask(state, f"Turno {i+1}")
    
    # El modelo debe de recordar o responder de forma coherente
    r = conversation.ask(state, "¿Cuál es mi color favorito?")
    assert isinstance(r, str)
    #assert "azul" in r.lower() or "no recuerdo" in r.lower()
    if llm.USE_SIMULATED:
        # Solo se verifica que sea string, no el contenido
        assert isinstance(r, str)
    else:
        # Aqui se Verifica con el contenido real del LLM
        assert "azul" in r.lower() or "no recuerdo" in r.lower()

