# /raiz/tests/conversation.py

# Se define un máximo de turnos para mantener en la historia
MAX_HISTORY = 10  # El límite de la cantidad de turnos que se desea mantener en la memoria.

class ConversationState:
    def __init__(self):
        # Historial de conversación
        self.history = []
        self.intents = []
        self.input_tokens = []
        self.output_tokens = []
        self.request_ids = []

    def update_state(self, user_input, assistant_response):
        if user_input.startswith("/"):
            self.intents.append(user_input.split()[0])
        """
        Actualiza el estado de la conversación añadiendo un turno de usuario y su respuesta correspondiente del asistente.

        Si el historial supera el máximo permitido, se realiza un truncado.
        """
        # Añadir el turno del usuario y la respuesta del asistente
        self.history.append({'role': 'user', 'content': user_input})
        self.history.append({'role': 'assistant', 'content': assistant_response})

        self.input_tokens.append(len(user_input.split()))
        self.output_tokens.append(len(assistant_response.split()))

        # Si el número total de mensajes (usuarios + asistentes) supera el límite, truncamos el historial
        if len(self.history) > MAX_HISTORY * 2:
            self.history = self.history[-MAX_HISTORY * 2:] 
            self.input_tokens = self.input_tokens[-MAX_HISTORY:]  # Mantiene solo los últimos MAX_HISTORY turnos completos
            self.output_tokens = self.output_tokens[-MAX_HISTORY:]

    def get_recent_history(self):
        """
        Obtiene el historial reciente de la conversación, limitando la cantidad de mensajes.
        Este método puede ser útil si se esta construyendo el mensaje de entrada para el modelo.
        """
        return self.history[-MAX_HISTORY*2:]  # Devuelve los últimos MAX_HISTORY turnos completos (usuario + asistente)
    
    def mostrar_metricas_tokens(self):
        import statistics
        if self.input_tokens:
            p50_in = statistics.median(self.input_tokens)
            p95_in = sorted(self.input_tokens)[max(0, int(0.95*len(self.input_tokens))-1)]
        else:
            p50_in = p95_in = 0
        if self.output_tokens:
            p50_out = statistics.median(self.output_tokens)
            p95_out = sorted(self.output_tokens)[max(0, int(0.95*len(self.output_tokens))-1)]
        else:
            p50_out = p95_out = 0

        print(f"Tokens por turno | entrada p50/p95: {p50_in}/{p95_in} | salida p50/p95: {p50_out}/{p95_out}")

