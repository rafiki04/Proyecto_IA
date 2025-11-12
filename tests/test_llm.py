import time
import pytest
from services.llm import generate
from core.conversation import ConversationState
from core.prompting import build_messages

def test_llm_basic():
    conv = ConversationState()
    user_input = "Hola, ¿puedes presentarte?"
    messages = build_messages(conv.get_recent_history(), user_input)
    
    start = time.time()
    response = generate(messages)
    end = time.time()
    
    conv.update_state(user_input, response)
    
    # Validaciones
    assert response is not None
    assert len(response) > 0
    
    latency = end - start
    print(f"✅ Latencia: {latency:.2f}s | Respuesta: {response}")
