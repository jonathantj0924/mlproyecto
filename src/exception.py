import sys
# sys: Es una librería interna de Python que nos permite interactuar 
# directamente con el motor de Python y extraer información del sistema.

def error_message_detail(error, error_detail: sys):
    """
    ¿Qué hace esta función?
    Extrae la 'radiografía' del error: el nombre del archivo, 
    la línea exacta donde falló y el mensaje de error.
    """
    
    # error_detail.exc_info() devuelve 3 cosas sobre el error:
    # 1. Tipo de error (no lo usamos, por eso ponemos '_')
    # 2. Valor del error (no lo usamos, por eso ponemos '_')
    # 3. exc_tb (Traceback): El 'rastro' del error donde está guardada la línea y el archivo.
    _, _, exc_tb = error_detail.exc_info()
    
    # Extraemos el nombre del archivo donde ocurrió el fallo
    file_name = exc_tb.tb_frame.f_code.co_filename
    
    # Construimos un mensaje súper claro y profesional con los 3 datos:
    error_message = "Error en el script: [{0}] en la línea: [{1}] con mensaje: [{2}]".format(
        file_name,           # {0} -> Nombre del archivo
        exc_tb.tb_lineno,    # {1} -> Número de línea exacta
        str(error)           # {2} -> Mensaje de error original
    )
    
    return error_message


class CustomException(Exception):
    """
    Nuestra propia clase de excepción personalizada.
    Hereda de 'Exception' (la clase madre de todos los errores en Python).
    """
    def __init__(self, error_message, error_detail: sys):
        # super().__init__: Inicializa la clase Exception original de Python
        super().__init__(error_message)
        
        # Generamos nuestro mensaje detallado usando la función de arriba
        self.error_message = error_message_detail(error_message, error_detail=error_detail)

    def __str__(self):
        # Cuando alguien imprima el error (print), mostrará nuestro mensaje detallado
        return self.error_message
