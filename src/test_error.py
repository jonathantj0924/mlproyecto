####Pruebas de error para juoyter notebook 
### probamos el archivo de error en juoyter notebook

import sys
from src.exception import CustomException

def funcion_con_error():
    try:
        print("Ejecutando función dentro de test_error.py...")
        calculo = 10 / 0
        return calculo
    except Exception as e:
        # ¡El try-except está ADENTRO del archivo .py!
        raise CustomException(e, sys)


# 👇 AGREGA ESTO AL FINAL:
if __name__ == "__main__":
    funcion_con_error()

#Si se lo ejecuta en la terminal si fucniona da el archivo y la linea que tiene ese error'
#.\venv\python.exe 
