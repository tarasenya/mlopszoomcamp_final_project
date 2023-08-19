"""
Flask web service to serve a registered model using mlflow server
"""
import os

import mlflow
import pandas as pd
from flask import Flask, jsonify, request
from mlflow import MlflowClient
from mlflow.pyfunc import PyFuncModel

MLFLOW_HOST = os.getenv('MLFLOW_HOST', 'http://0.0.0.0:5000')
MODEL_NAME = 'HeartStroke'

APP_HOST = os.getenv('APP_HOST', '0.0.0.0')
APP_PORT = 9696

mlflow.set_tracking_uri(MLFLOW_HOST)
client = MlflowClient(mlflow.get_tracking_uri())

run_id = client.get_latest_versions(MODEL_NAME)[0].run_id
logged_model = f'runs:/{run_id}/model'
model = mlflow.pyfunc.load_model(logged_model)

app = Flask('heart-stroke-prediction')


def predict(patient_info: dict, heartstroke_model: PyFuncModel) -> bool:
    """
    Using 'patient_info' dictionary with information about a patient predict whether he/she gets
    a heart stroke
    :patient_info: information with fields defined in the initial csv
    :heartstroke_model: mlflow model defined in PyFuncModel flavour
    """
    prediction = heartstroke_model.predict(pd.DataFrame(patient_info, index=[0]))
    return prediction[0] == 1


@app.route('/predict', methods=['POST'])
def predict_endpoint():
    """
    Prediction endpoint
    """
    patient_info = request.get_json()
    global model  # pylint: disable=global-statement
    global run_id  # pylint: disable=global-statement

    potential_new_run_id = client.get_latest_versions(MODEL_NAME)[0].run_id
    if potential_new_run_id != run_id:
        new_logged_model = f'runs:/{potential_new_run_id}/model'
        model = mlflow.pyfunc.load_model(new_logged_model)
        run_id = potential_new_run_id

    prediction = predict(patient_info, model)

    result = {
        'risk_of_heart_attack': str(prediction),
        'model_version': potential_new_run_id,
    }
    print(result)
    return jsonify(result)


if __name__ == '__main__':
    app.run(host=APP_HOST, port=APP_PORT)
