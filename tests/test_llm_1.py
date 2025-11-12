#raiz/tests/test_llm_1.py

from services.llm import generate
from core.conversation import ConversationState
from core.prompting import build_messages

conv = ConversationState()
user_input = "Hola, ¿puedes presentarte?"
messages = build_messages(conv.get_recent_history(), user_input)
response = generate(messages)
conv.update_state(user_input, response)

print("AI Copilot:", response)
