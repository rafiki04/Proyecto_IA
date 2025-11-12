# tests/test_e2e_ana.py
import pytest
from core import conversation

def test_e2e_nombre_ana():
    state = conversation.init_state()

    # Flujo de prueba
    r1 = conversation.ask(state, "Me llamo Ana")
    assert isinstance(r1, str)
    
    r2 = conversation.ask(state, "Hola Ana")
    assert isinstance(r2, str)
    
    r3 = conversation.ask(state, "¿Cómo me llamo?")
    assert isinstance(r3, str)

    # Si es un LLM real se valida que responda correctamente
    if not conversation.llm.USE_SIMULATED:
        assert "ana" in r3.lower() or "no recuerdo" in r3.lower()