import os
import sys
from dataclasses import dataclass

#from catboost import CatBoostRegressor Comentamos para correr
from sklearn.ensemble import (
    AdaBoostRegressor,
    GradientBoostingRegressor,
    RandomForestRegressor,
)

from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor
from xgboost import XGBRegressor


from src.exception import CustomException
from src.logger import logging
from src.utils import save_object, evaluate_models


@dataclass
class ModelTrainerConfig:
    trained_model_file_path: str = os.path.join("artifacts", "model.pkl")


class ModelTrainer:
    def __init__(self):
        self.model_trainer_config = ModelTrainerConfig()

    def initiate_model_trainer(self, train_array, test_array):
        try:
            logging.info("[model_trainer.py] 1.- Dividiendo datos de entrenamiento y prueba.")
            
            # Separamos las variables predictoras (X) de la variable objetivo (y)
            # Recordar que la última columna ([:, -1]) es la nota de matemáticas 'math_score'
            X_train, y_train, X_test, y_test = (
                train_array[:, :-1],
                train_array[:, -1],
                test_array[:, :-1],
                test_array[:, -1],
            )

            # Diccionario con todos los algoritmos a evaluar
            models = {
                "Random Forest": RandomForestRegressor(),
                "Decision Tree": DecisionTreeRegressor(),
                "Gradient Boosting": GradientBoostingRegressor(),
                "Linear Regression": LinearRegression(),
                "K-Neighbors Regressor": KNeighborsRegressor(),
                "XGBRegressor": XGBRegressor(),
                #"CatBoosting Regressor": CatBoostRegressor(verbose=False), #comentamos para correr el
                "AdaBoost Regressor": AdaBoostRegressor(),
            }

            #parametros para obtimizar los modelos son las perillas de cada modelo movemos para ajustarlo 
            # ver el notebook pruebas ahi etsa todo 
            #la explicaicon de lo que significa cada parametro
            params = {
                "Decision Tree": {
                    'criterion': ['squared_error', 'friedman_mse', 'absolute_error', 'poisson'],
                    # 'splitter': ['best', 'random'],
                    # 'max_features': ['sqrt', 'log2'],
                },
                "Random Forest": {
                    # 'criterion': ['squared_error', 'friedman_mse', 'absolute_error', 'poisson'],
                    # 'max_features': ['sqrt', 'log2', None],
                    'n_estimators': [8, 16, 32, 64, 128, 256]
                },
                "Gradient Boosting": {
                    # 'loss': ['squared_error', 'huber', 'absolute_error', 'quantile'],
                    'learning_rate': [.1, .01, .05, .001],
                    'subsample': [0.6, 0.7, 0.75, 0.8, 0.85, 0.9],
                    # 'criterion': ['squared_error', 'friedman_mse'],
                    # 'max_features': ['auto', 'sqrt', 'log2'],
                    'n_estimators': [8, 16, 32, 64, 128, 256]
                },
                "Linear Regression": {},
                "K-Neighbors Regressor": {
                    'n_neighbors': [5, 7, 9, 11]
                    # 'weights': ['uniform', 'distance'],
                    # 'algorithm': ['ball_tree', 'kd_tree', 'brute']
                },
                "XGBRegressor": {
                    'learning_rate': [.1, .01, .05, .001],
                    'n_estimators': [8, 16, 32, 64, 128, 256]
                },
                "CatBoosting Regressor": {
                    'depth': [6, 8, 10],
                    'learning_rate': [0.01, 0.05, 0.1],
                    'iterations': [30, 50, 100]
                },
                "AdaBoost Regressor": {
                    'learning_rate': [.1, .01, 0.5, .001],
                    # 'loss': ['linear', 'square', 'exponential'],
                    'n_estimators': [8, 16, 32, 64, 128, 256]
                }
            }







            logging.info("[model_trainer.py] 2.- Evaluando todos los modelos...")
            # evaluate_models entrena cada uno y nos retorna un diccionario {nombre: r2_score}
            model_report:  dict = evaluate_models( # esta funcion esta contenida en utils 
                X_train=X_train, 
                y_train=y_train,
                X_test=X_test,
                y_test=y_test,
                models=models,
                params = params
            )

            # Obtener el puntaje más alto
            best_model_score = max(sorted(model_report.values()))

            # Obtener el nombre del modelo que sacó ese puntaje más alto
            best_model_name = list(model_report.keys())[
                list(model_report.values()).index(best_model_score)
            ]

            best_model = models[best_model_name]

            # Umbral de calidad: si el mejor modelo no supera el 60% de precisión, se rechaza
            if best_model_score < 0.6:
                raise CustomException("No se encontró un modelo óptimo (Score menor a 0.6)")

            logging.info(f"[model_trainer.py] 3.- Mejor modelo encontrado: {best_model_name} con score: {best_model_score}")

            # Guardamos el mejor modelo físicamente en artifacts/model.pkl
            #save object viene de 
            save_object(
                file_path=self.model_trainer_config.trained_model_file_path,
                obj=best_model,
            )

            # Hacemos la predicción final en el conjunto test y calculamos R2 final
            # guardar en artefactos con el nombre  artifacts/model.pkl

            predicted = best_model.predict(X_test)
            r2_square = r2_score(y_test, predicted)

            return r2_square

        except Exception as e:
            raise CustomException(e, sys)


    
