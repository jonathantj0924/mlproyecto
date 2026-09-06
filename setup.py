from setuptools import find_packages, setup
from typing import List #Antes (Python 3.8 y anteriores): Python obligaba a importar List con mayúscula
#Ahora (Python 3.9 en adelante): Python mejoró y ya NO necesitas importar nada


"""
    Oye, todo el código de Jonathan no son solo archivos sueltos,
    ¡es una librería/paquete oficial llamado mlproject!"

    venv: El espacio seguro y aislado para no ensuciar tu computadora con descargas.
    setup.py: El carnet de identidad que convierte tu carpeta en un paquete oficial de Python.
    src: El taller organizado donde programas todas las partes de tu inteligencia artificial.

     Este archivo (setup.py) es el "Carnet de Identidad" de tu proyecto.
    Convierte todo el código que escribas en la carpeta 'src' en un 
    PAQUETE OFICIAL INSTALABLE de Python.
    CONCEPTOS CLAVE:
    1. venv: La mochila/caja aislada para no ensuciar tu computadora con librerías globales.
    2. setup.py: El empaque oficial que permite importar código desde cualquier archivo.
    3. src: El taller/laboratorio donde vive toda la lógica de tu Inteligencia Artificial.
"""



def obtener_requisitos(ruta: str)-> List[str]: 
    """
        Esta funcion retorna una lista de requisitos
        
        ¿Qué hace esta función?
        Lee el archivo 'requirements.txt', extrae los nombres de las librerías 
        que necesitamos (pandas, numpy, etc.) y las devuelve en una lista limpia.
    """

    #
    HYPEN_E_DOT = '-e .'
    requisitos = []
    
    with open(ruta)  as file_obj:
        requisitos = file_obj.readlines()
        requisitos = [i.replace("\n", "") for i in requisitos]

        # Si existe '-e .', lo eliminamos de la lista
        # Si encuentra '-e .', lo quitamos de la lista.
        # ¿Por qué? Porque '-e .' no es una librería de internet (PyPI),
        # solo es el activador para que pip ejecute este setup.py.

        if HYPEN_E_DOT in requisitos:
            requisitos.remove(HYPEN_E_DOT)

    return requisitos



setup(
    name='mlproject',                         # Nombre de tu proyecto / paquete
    version='0.0.1',                          # Versión inicial
    author='Jonathan',                        # Tu nombre
    author_email='jonnathan_2409@hotmail.com',# Tu correo
    packages=find_packages(),                 # Busca automáticamente todas las carpetas con __init__.py carga SRC
    install_requires= obtener_requisitos('requirements.txt') # Carga las librerías necesarias
)