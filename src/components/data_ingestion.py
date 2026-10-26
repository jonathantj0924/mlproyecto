import os
import sys
from src.exception import CustomException
from src.logger import logging #contruyo para almacenar los log de los archivos
import pandas as pd
from sklearn.model_selection import train_test_split
from dataclasses import dataclass

#importamos para realizar las pruebas
from src.components.data_transformation  import DataTransformation
from src.components.data_transformation import DataTransformationConfig # e


@dataclass
class DataIngestionConfig:
    train_data_path: str = os.path.join('artifacts', "train.csv")
    test_data_path: str = os.path.join('artifacts', "test.csv")
    raw_data_path: str = os.path.join('artifacts', "data.csv")



class DataIngestion:
    """
    Esta es la clase trabajadora (la fábrica).
    Se encarga de:
    1. Leer los datos originales (stud.csv).
    2. Crear la carpeta 'artifacts/' en tu disco.
    3. Guardar la copia original (data.csv).
    4. Dividir en 80% entrenamiento (train.csv) y 20% prueba (test.csv).
    """

    def __init__(self):
        # Conectamos la libreta de direcciones con las rutas que definimos arriba
        self.ingestion_config = DataIngestionConfig()

    def initiate_data_ingestion(self):
        logging.info("1. Iniciando el proceso de Ingesta de Datos...")
        
        try:
            # 1. Leemos el archivo de datos original
            # (Asegúrate de tener el archivo stud.csv dentro de notebook/data/)
            df = pd.read_csv('notebook/data/stud.csv') #solo cambiamos esta linea para conectarnos a otra fuente de dato
            logging.info("2. Dataset leído exitosamente como DataFrame de Pandas.")

            # 2. Creamos físicamente la carpeta 'artifacts/' en tu computadora
            # 'os.path.dirname' extrae solo el nombre de la carpeta: 'artifacts' esto retorna nada mas 
            # 'exist_ok=True' evita errores si la carpeta ya existía de antes
            os.makedirs(
                os.path.dirname(self.ingestion_config.train_data_path), #ver ejemplo de jupyter notebook solo es el nombre de la carpeta
                exist_ok=True
            )

            # 3. Guardamos la copia completa original (raw data) en artifacts/data.csv
            df.to_csv(
                self.ingestion_config.raw_data_path, #ruta donde se guardara ela archvio  
                index=False,
                header=True
            )
            logging.info("3. Archivo con datos originales (raw data) guardado.")

            # 4. Dividimos los datos: 80% para entrenar y 20% para evaluar (test_size=0.2)
            # random_state=42 asegura que siempre corte los datos de la misma forma exacta
            logging.info("4. Iniciando división de datos en Train y Test...")

            train_set, test_set = train_test_split(df, test_size=0.2, random_state=42)

            # 5. Guardamos físicamente los dos archivos divididos en el disco
            train_set.to_csv(
                self.ingestion_config.train_data_path, ##ruta donde se guardara el archivo
                index=False,
                header=True
            )
            test_set.to_csv(self.ingestion_config.test_data_path, index=False, header=True)

            logging.info("5. Ingesta de datos completada con éxito total.")

            # 6. Devolvemos las dos rutas finales para que el siguiente componente
            #    (Data Transformation) sepa dónde encontrar los archivos
            return (
                self.ingestion_config.train_data_path,
                self.ingestion_config.test_data_path
            )

        except Exception as e:
            # Si algo falla (ej: no encuentra stud.csv), nuestra alarma nos dice la línea exacta
            raise CustomException(e, sys)


from src.components.data_transformation import DataTransformation

if __name__ == "__main__":

    # PASO 1: Ejecutar la ingesta de datos

    # Retorna las rutas donde quedaron guardados train.csv y test.csv
    obj = DataIngestion()
    train_data, test_data = obj.initiate_data_ingestion() #metodo dentro de la clase

    # PASO 2: Pasar esas rutas a la transformación de datos
    # DataTransformation lee los CSV, aplica pipelines y guarda preprocessor.pkl
    data_transformation = DataTransformation()
    data_transformation.initiate_data_transformation(train_data, test_data)








