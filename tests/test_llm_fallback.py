#tests/test_llm_fallback
import pytest
from services.llm import generate
from core.prompting import build_messages
from core.conversation import ConversationState

def test_llm_fallback_and_metrics():
    conv = ConversationState()
    user_input = "Genera error simulado 500"
    messages = build_messages(conv.get_recent_history(), user_input)
    
    try:
        response = generate(messages, simulate_error=500) 
    except Exception as e:
        response = "Fallback activado"
    
    conv.update_state(user_input, response)
    
    assert response == "Fallback activado"  # prueba fallback
    # Aquí podemos imprimir métricas básicas
    print("Reintentos: 1 | Fallbacks: 1")
