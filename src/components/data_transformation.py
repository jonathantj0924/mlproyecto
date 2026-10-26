# proposito de la transfromacion es realizar ingenieria de catacteristicas 
#limpieza de datos 
#convertir las caracteriticsa categorica en carcateristicas numericas 



import os
import sys
from dataclasses import dataclass

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

# Importaciones de utilidades y manejo de excepciones personalizados del proyecto
from src.exception import CustomException
from src.logger import logging


from src.utils import save_object  # Función auxiliar para guardar objetos en archivos pickle VIENE DE ARCHVIO UTILS



@dataclass
class DataTransformationConfig:
    # Ruta donde se guardará el objeto preprocesador entrenado (en formato pickle)
    preprocessor_obj_file_path: str = os.path.join('artifacts', 'preprocessor.pkl')


class DataTransformation:
    def __init__(self):
        # Inicializa la configuración para obtener la ruta del archivo pickle del preprocesador
        self.data_transformation_config = DataTransformationConfig()

    def get_data_transformer_object(self):
        """
        Esta función es responsable de crear y retornar el objeto 'ColumnTransformer'
        que aplicará las transformaciones correctas a las columnas numéricas y categóricas.
        """
        try:
            # 1. Definición de características numéricas y categóricas según el análisis exploratorio (EDA)
            numerical_columns = ["writing_score", "reading_score"]
            categorical_columns = [
                "gender",
                "race_ethnicity",
                "parental_level_of_education",
                "lunch",
                "test_preparation_course",
            ]

            logging.info("[data_transformation.py] 1.- Definición de columnas numéricas y categóricas completada exitosamente.")

            # 2. Pipeline para variables numéricas:
            #    - Maneja valores faltantes rellenando con la 'mediana' (robusto ante valores atípicos/outliers).
            #    - Aplica estandarización (StandardScaler) para poner los datos en la misma escala.
            num_pipeline = Pipeline(
                steps=[
                    ("imputer", SimpleImputer(strategy="median")),
                    ("scaler", StandardScaler())
                ]
            )

            # 3. Pipeline para variables categóricas:
            #    - Maneja valores faltantes rellenando con el valor más frecuente ('most_frequent' / moda).
            #    - Convierte variables categóricas en numéricas usando One-Hot Encoding.
            #    - Aplica estandarización opcionalmente.
            cat_pipeline = Pipeline(
                steps=[
                    ("imputer", SimpleImputer(strategy="most_frequent")),
                    ("one_hot_encoder", OneHotEncoder()),
                    ("scaler", StandardScaler(with_mean=False))  # with_mean=False evita errores en matrices dispersas (sparse matrices)
                ]
            )

            logging.info("[data_transformation.py] 2.- Creación de pipelines numérico y categórico completada exitosamente.")

            # 4. Combinación de ambos pipelines usando ColumnTransformer
            preprocessor = ColumnTransformer(
                transformers=[
                    ("num_pipeline", num_pipeline, numerical_columns),
                    ("cat_pipeline", cat_pipeline, categorical_columns)
                ]
            )

            logging.info("[data_transformation.py] 3.- Configuración del ColumnTransformer completada exitosamente.")

            #returna este objeto que tiene inmersa la logica para transformar los datos
            return preprocessor

        except Exception as e:
            # Manejo de errores personalizado
            raise CustomException(e, sys)

    def initiate_data_transformation(self, train_path, test_path):
        """
        Esta función lee los datasets de entrenamiento y prueba, aplica el preprocesador,
        separa la variable objetivo (target) y guarda el objeto preprocesador en disco.
        """
        try:
            # Leer los archivos CSV de entrenamiento y prueba generados en la ingesta de datos
            train_df = pd.read_csv(train_path)
            test_df = pd.read_csv(test_path)

            logging.info("[data_transformation.py] 4.- Lectura de los datasets de entrenamiento y prueba completada exitosamente.")


            # Obtener el objeto ColumnTransformer configurado
            # llama y ejecuta la función que está arriba dentro de la misma clase
            # return preprocessor, guarda ese objeto resultante dentro de la variable llamada preprocessing_obj
            #Este objeto no es mas que pipeline ya lsito a utilizar
            preprocessing_obj = self.get_data_transformer_object()

            logging.info("[data_transformation.py] 5.- Obtención del objeto preprocesador completada exitosamente.")

            # Nombre de las columnas nada mas objetivo y numericas
            target_column_name = "math_score"
            numerical_columns = ["writing_score", "reading_score"]

            # Separar las características independientes (input features) de la variable objetivo (target) en train
            input_feature_train_df = train_df.drop(columns=[target_column_name], axis=1) #columnas caracteristicas todas menos la variable y
            target_feature_train_df = train_df[target_column_name]

            
            # Separar las características independientes de la variable objetivo en test
            input_feature_test_df = test_df.drop(columns=[target_column_name], axis=1)
            target_feature_test_df = test_df[target_column_name]

            logging.info("[data_transformation.py] 6.- Separación de variables independientes y objetivo completada exitosamente.")





            # Aplicar transformaciones: fit_transform en train y solo transform en test (para evitar data leakage)
            input_feature_train_arr = preprocessing_obj.fit_transform(input_feature_train_df)  #columnas caracteristicas todas menos la variable y retrona el data set transformado
            input_feature_test_arr = preprocessing_obj.transform(input_feature_test_df) #solo transform al data set

            logging.info("[data_transformation.py] 7.- Aplicación de transformaciones en train y test completada exitosamente.")

            # Concatenar las características transformadas con su respectiva variable objetivo (en formato numpy array)
            #concatenamos lascolumnas todas x y y en una sola .c_ es un alias de concatenacion
            ## Concatenamos las columnas de características y la columna objetivo en una sola matriz.
            # np.c_ es un alias de concatenación por columnas (equivalente a np.column_stack).


            train_arr = np.c_[input_feature_train_arr, np.array(target_feature_train_df)]
            test_arr = np.c_[input_feature_test_arr, np.array(target_feature_test_df)]

            # Guardar el objeto preprocesador usando la función auxiliar de utilidades

            #ESTA FUNCION NOS VIENE DE UTILS -  DE ESE ARCHIVO
            #que guarda?
            #Contenido: Objeto ColumnTransformer con dos pipelines (numérico y categórico) ya fit a los datos de entrenamiento.
            save_object(

                #Esto es el path contruido en el metodo anteiror arriba 
                file_path=self.data_transformation_config.preprocessor_obj_file_path,
                obj=preprocessing_obj
            )

            logging.info("[data_transformation.py] 8.- Guardado del objeto preprocesador completado exitosamente.")


            #Returna los data set concatenados
            return (
                train_arr, #esta concatenado arriba train contiene x y y
                test_arr, #esta concatebado arriba contiene x y y del set de entrenamiento
                self.data_transformation_config.preprocessor_obj_file_path,
                #Ruta donde se guardará el objeto preprocesador entrenado (en formato pickle)
            )

        except Exception as e:
            raise CustomException(e, sys)