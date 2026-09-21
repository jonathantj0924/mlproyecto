"""
=============================================================================
PROYECTO: mlproject (End to End Data Science)
ARCHIVO: src/logger.py
DESCRIPCIÓN:
    Este archivo es la "Caja Negra" o el "Diario Secreto" de tu proyecto.
    Registra TODO lo que ocurre mientras se ejecuta el programa:
    - Cuándo inicia un proceso
    - Qué datos se cargaron
    - Si ocurrió una advertencia o un error
    Todo queda guardado con fecha, hora exacta y número de línea en un archivo .log
=============================================================================
"""

import logging
import os
from datetime import datetime

# 1. Creamos un nombre de archivo único usando la fecha y hora actual.
#    Ejemplo: '09_20_2026_19_45_12.log'
#    %m = mes, %d = día, %Y = año, %H = hora, %M = minuto, %S = segundo
LOG_FILE = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"

# 2. Definimos la ruta de la carpeta donde se guardarán los registros:
#    'os.getcwd()' obtiene la carpeta actual del proyecto.
#    Unimos: Carpeta_Actual / 'logs' / '09_20_2026_19_45_12.log'
logs_path = os.path.join(os.getcwd(), "logs", LOG_FILE)

# 3. 'os.makedirs' crea la carpeta 'logs' si todavía no existe.
#    'exist_ok=True' significa: si la carpeta ya existe, no des error, sigue adelante.
os.makedirs(logs_path, exist_ok=True)

# 4. Ruta completa del archivo final dentro de la carpeta:
LOG_FILE_PATH = os.path.join(logs_path, LOG_FILE)

# 5. CONFIGURACIÓN DEL SISTEMA DE REGISTRO (logging.basicConfig):
logging.basicConfig(
    # ¿Dónde se guardan los mensajes?: En el archivo que creamos arriba
    filename=LOG_FILE_PATH,
    
    # ¿Cómo se verá cada línea del mensaje?:
    # [ Fecha y Hora ] Línea - NombreDelModulo - NivelDeImportancia - Mensaje
    # Ejemplo: [ 2026-09-20 19:45:12,123 ] 15 root - INFO - La ingesta de datos ha comenzado
    format="[ %(asctime)s ] %(lineno)d %(name)s - %(levelname)s - %(message)s",
    
    # Nivel mínimo de mensajes a guardar (INFO = guarda mensajes informativos, advertencias y errores)
    level=logging.INFO,
)


# =============================================================================
# PRUEBA RÁPIDA PARA VERIFICAR QUE FUNCIONA:
# =============================================================================
# if __name__ == "__main__":
#     # Escribimos nuestro primer mensaje de prueba en el registro
#     logging.info("¡El sistema de Logging ha iniciado exitosamente!")
# es solo para que inicie el archivo de los log la carpet se cree y el primer log