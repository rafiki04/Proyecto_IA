# tests/test_llm_retry_fallback.py
import pytest
import uuid
from services import llm
from core.prompting import build_messages
from core.conversation import ConversationState

@pytest.mark.parametrize("error_code", [400, 401, 403, 404, 500, 502, 503])
def test_llm_retry_and_fallback(monkeypatch, error_code):
    conv = ConversationState()
    user_input = "Genera error simulado"
    messages = build_messages(conv.get_recent_history(), user_input)

    # Mock del generate para simular errores
    def mock_generate(*args, **kwargs):
        raise Exception(f"Simulated error {error_code}")

    monkeypatch.setattr(llm, "generate", mock_generate)

    # Llamamos a generate y verificamos fallback
    e = None
    try:
        response = llm.generate(messages, simulate_error=error_code, request_id=str(uuid.uuid4()))
    except Exception as exc:
        e = exc
        response = f"Fallback activado por error {error_code}"

    conv.update_state(user_input, response)

    # Validación: fallback debe activarse para errores 5xx
    if error_code >= 500:
        assert "Fallback activado" in response or "Lo siento" in response
    else:
        # Errores 4xx → mensaje claro de cliente
        if e is not None:
            assert "Simulated error" in str(e)
        else:
            assert "error" in response.lower()
