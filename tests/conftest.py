#codigo para configuracion pytests ademas de configurar el uso de el modelo online u offline con USE_REAL_LLM=false.



#/raiz/tests/conftest.py
import os
import sys

# Agrega la carpeta raíz del proyecto al sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Importa el módulo del cliente LLM
import services.llm as llm

# Controla si se usa el LLM real o el modo offline simulado
use_real = os.getenv("USE_REAL_LLM", "true").lower() == "true"

if not use_real:
    llm.client = None  # fuerza el modo offline para pruebas rápidas y seguras
