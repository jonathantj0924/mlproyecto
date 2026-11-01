# src/utils.py
"""
Módulo de utilidades comunes para el proyecto.

Contiene funciones para serializar y deserializar objetos Python usando
`dill`, lo que permite guardar pipelines de scikit‑learn, modelos entrenados
u otros objetos que no son soportados por `pickle` estándar.
"""

import os
import dill


def save_object(obj, file_path):
    """
    Guarda *obj* en la ruta *file_path* usando `dill`.

    - Crea los directorios intermedios si no existen.
    - Sobrescribe el archivo si ya está presente.

    Parámetros
    ----------
    obj : any
        Objeto Python a serializar (por ejemplo, un ColumnTransformer).
    file_path : str
        Ruta completa del archivo donde se guardará el objeto (debe terminar
        con ".pkl" o extensión similar).
    """
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "wb") as f:
        dill.dump(obj, f)


def load_object(file_path):
    """
    Carga y retorna el objeto previamente guardado con ``save_object``.

    Parámetro
    ---------
    file_path : str
        Ruta del archivo ".pkl" a leer.
    """
    with open(file_path, "rb") as f:
        return dill.load(f)



#CReacion de una metrica par evaluar modelos la llamamos desde el otro archivo
from sklearn.metrics import r2_score

def evaluate_models(X_train, y_train, X_test, y_test, models):
    """
    Entrena múltiples modelos y evalúa su rendimiento con R2 Score.
    """
    try:
        report = {}

        for i in range(len(list(models))):
            model = list(models.values())[i]

            # 1. Entrenar modelo
            model.fit(X_train, y_train)

            # 2. Predecir en datos de prueba
            y_test_pred = model.predict(X_test)

            # 3. Calcular métrica R2
            test_model_score = r2_score(y_test, y_test_pred)

            # 4. Guardar puntaje en el reporte
            report[list(models.keys())[i]] = test_model_score

        return report

    except Exception as e:
        raise CustomException(e, sys)