"""
Module with models' training flows
"""
import os
import pickle
import shutil
import tempfile
from typing import Any, Union
from datetime import datetime

import mlflow
import pandas as pd
import lightgbm
from lightgbm import LGBMClassifier
from prefect.flows import flow
from prefect.tasks import task
from mlflow.tracking import MlflowClient
from sklearn.pipeline import Pipeline

from src.utils.metrics import calculate_metrics_for_classifier
from src.utils.constants import (
    MODEL_NAME,
    EXPERIMENT_NAME,
    HEART_STROKE_DATA,
    INITIAL_PARAMETERS_FOR_LGBM_CLF,
)
from src.utils.transformators import create_column_transformator

MLFLOW_HOST = os.getenv('MLFLOW_HOST', 'http://0.0.0.0:5000')
client = MlflowClient(MLFLOW_HOST)


@task()
def get_data(data_name: str) -> pd.DataFrame:
    """
    Get data from heart-stroke-data S3 bucket
    :data_name: name of a csv file
    :return: pandas data frame created from a csv file
    """
    s3_bucket_url = os.getenv('S3_BUCKET_URL', 'http://localhost:4566')
    return pd.read_csv(
        os.path.join(s3_bucket_url, f'{HEART_STROKE_DATA}/{data_name}'), index_col="id"
    )


# @task()
def train_model_using_hyperopt():
    """Training models using hyperopt"""
    print('Train')


def pipeline_fit_transformation(data: pd.DataFrame) -> tuple[pd.DataFrame, Pipeline]:
    """
    Fit pipeline and transform features. Pipeline is defined as an output of
    'create_column_transformator' function
    :data: feature matrix
    :return: transformed feature matrix
    """
    _transformation_pipeline = create_column_transformator()
    return _transformation_pipeline.fit_transform(data), _transformation_pipeline


@task()
def pipeline_transform(fitted_pipeline: Pipeline, data: pd.DataFrame) -> pd.DataFrame:
    """
    Transform features using 'fitted_pipeline'pipeline
    :fitted_pipeline: fitted pipeline used to transform 'data'.
    :data: feature matrix
    :return: transformed feature matrix
    """
    return fitted_pipeline.transform(data)


# @task()
def quickly_perform_grid_search_cv():
    """
    Training model using RandomizedGridSearchCV
    """
    print('Qucikly train')


def pickling_obj(obj: Any) -> str:
    """
    Pickle an object and put it to a temporary directory
    :obj: python object
    :return: path to a pickled object
    """
    dir_path = tempfile.mkdtemp()
    with open(os.path.join(dir_path, 'preprocess_pipeline.pkl'), 'wb') as f_out:
        pickle.dump(obj, f_out)

    return dir_path


@task(log_prints=True)
def train_model(
    params: dict, data: pd.DataFrame, experiment_name: str, tracking_server_host: str
) -> str:
    """
    Prefect task to train a LGBMClassifier model defined by 'params' parameters on 'data'.
    This should be done in experiment with a name 'experiment_name',
    mlflow server is run on 'tracking_server_host'
    :params: parameters to define LGBMClassifier
    :data: data to train a model on
    :experiment_name: name of a mlflow experiment
    :tracking_server_host:  mlflow is run on this host
    """
    mlflow.set_tracking_uri(tracking_server_host)
    print(tracking_server_host)
    mlflow.set_experiment(experiment_name=experiment_name)

    feature_data, transformation_pipeline = pipeline_fit_transformation(data)
    target_variable = data['stroke']
    temp_dir_path = pickling_obj(transformation_pipeline)

    with mlflow.start_run() as current_run:
        run_id = current_run.info.run_id
        mlflow.log_params(params)
        model_to_fit = LGBMClassifier(**params)
        model_to_fit.fit(feature_data, target_variable)
        print("Logging artifacts")
        mlflow.log_artifacts(temp_dir_path)
        print('Model is fitted')
        final_pipeline = Pipeline(
            [
                ('transformation_pipeline', transformation_pipeline),
                ('model', model_to_fit),
            ]
        )

        conda_env = mlflow.sklearn.get_default_conda_env()
        conda_env["dependencies"] = [f'lightgbm=={lightgbm.__version__}'] + conda_env[
            "dependencies"
        ]
        recall_1, precision_1, recall_0, precision_0 = calculate_metrics_for_classifier(
            model_to_fit, feature_data, target_variable
        )
        mlflow.log_metric('recall_1', recall_1)
        mlflow.log_metric('precision_1', precision_1)
        mlflow.log_metric('recall_0', recall_0)
        mlflow.log_metric('precision_0', precision_0)
        mlflow.sklearn.log_model(
            final_pipeline,
            'model',
            registered_model_name="HeartStroke",
            conda_env=conda_env,
            code_paths=[os.path.dirname(os.path.dirname(os.path.realpath(__file__)))],
        )
        print('Model has been logged')
    shutil.rmtree(temp_dir_path)
    return run_id


@task()
def register_model(run_id: str, tracking_server_host: str, model_name: str) -> str:
    """
    Task to register a model defined within a run with 'run_id' with a name 'model_name' within a
    mlflow server run on 'tracking_server_host'
    :run_id: run id of a mlflow run
    :model_name: name of a model
    :tracking_server_host:  mlflow is run on this host
    """
    mlflow.set_tracking_uri(tracking_server_host)
    model_version = mlflow.register_model(
        model_uri=f"runs:/{run_id}/models", name=model_name
    ).version
    return model_version


@flow(name="TrainInitialModel")
def train_initial_model():
    """
    Prefect flow to train an initial model
    """
    data = get_data('initial_heart_stroke_data.csv')
    run_id = train_model(
        INITIAL_PARAMETERS_FOR_LGBM_CLF, data, EXPERIMENT_NAME, MLFLOW_HOST
    )
    model_version = register_model(run_id, MLFLOW_HOST, MODEL_NAME)
    client.transition_model_version_stage(
        name="HeartStroke", version=model_version, stage="Production"
    )


@flow(name='RetrainModel')
def retrain_model_using_new_data(filename_new_data: Union[pd.DataFrame, None]):
    """
    Prefect flow to retrain a model using new data.
    """
    if not filename_new_data:
        filename_new_data = f"heart_stroke_{datetime.today().strftime('%Y-%m-%d')}.csv"

    data = get_data(filename_new_data)

    run_id = train_model(
        INITIAL_PARAMETERS_FOR_LGBM_CLF, data, EXPERIMENT_NAME, MLFLOW_HOST
    )
    model_version = register_model(run_id, MLFLOW_HOST, MODEL_NAME)
    client.transition_model_version_stage(
        name="HeartStroke", version=model_version, stage="Production"
    )


if __name__ == '__main__':
    train_initial_model()
