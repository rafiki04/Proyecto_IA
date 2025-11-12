import gradio as gr
from core.conversation import ConversationState, ask, init_state
from services import llm

# Inicializar estado y conversación
state = init_state()
conv_state = ConversationState()
state["history"] = conv_state.history

# Lista para mantener el chat en la UI
chat_history = []

# Función para responder usando la lógica de conversación
def responder(input_text):
    respuesta = ask(state, input_text)
    # Destacar fallback visible
    if "Lo siento, no puedo" in respuesta:
        respuesta = f"{respuesta}"
    return respuesta

# Función para enviar mensaje desde la UI
def enviar(input_text):
    if not input_text.strip():
        return chat_history, ""
    
    resp = responder(input_text)
    chat_history.append((input_text, resp))
    
    # Mostrar límite de turnos
    max_turns = 20
    if len(conv_state.history) // 2 > max_turns:
        aviso = f" Has alcanzado el límite de {max_turns} turnos. La sesión se reiniciará en el próximo mensaje."
        chat_history.append(("", aviso))
    
    return chat_history, ""

# Función para mostrar métricas del modelo
def mostrar_metricas_ui():
    from io import StringIO
    import sys

    # Se redirige salida estandar temporalmente para capturar print
    old_stdout = sys.stdout
    sys.stdout = mystdout = StringIO()

    llm.mostrar_metricas()

    sys.stdout = old_stdout
    return mystdout.getvalue()

# UI con Gradio
with gr.Blocks() as demo:
    gr.Markdown("## AI Copilot - Chatbot MVP")
    
    chatbot = gr.Chatbot()
    msg = gr.Textbox(label="Escribe tu mensaje aquí")
    submit = gr.Button("Enviar")
    metrics_btn = gr.Button("Mostrar métricas del modelo")
    metrics_output = gr.Textbox(label="Métricas", interactive=False)
    
    submit.click(enviar, [msg], [chatbot, msg])
    metrics_btn.click(mostrar_metricas_ui, [], metrics_output)

# Lanzar la UI
demo.launch()
