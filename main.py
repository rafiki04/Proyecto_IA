# raiz/main.py
#Permite pasar simulate_error y request_id (útil para testing).
#Captura excepciones y devuelve un mensaje de fallback si ocurre algún error.

from typing import List, Dict, Optional
from services import llm

def generate(messages: List[Dict[str, str]], simulate_error: Optional[int] = None, request_id: Optional[str] = None) -> str:
    """
    Wrapper simple para tests: permite pasar simulate_error y request_id.
    """
    try:
        return llm.generate(messages, simulate_error=simulate_error, request_id=request_id)
    except Exception as e:
        # Si se produce excepción (p. ej. simulate_error) devolvemos un fallback
        # con la info de excepción para los tests que esperan fallback visible.
        rid = request_id or "no-request-id"
        return f"fallback activado: {str(e)} (request_id={rid})"
