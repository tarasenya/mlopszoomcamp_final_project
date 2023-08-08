import pickle
from typing import Any

from lightgbm import LGBMClassifier
import lightgbm
from prefect.flows import flow
from prefect.tasks import task
import os
import pandas as pd
import mlflow
from mlflow.tracking import MlflowClient
from sklearn.pipeline import Pipeline
import tempfile
import shutil

from src.utils.metrics import calculate_metrics_for_classifier
from src.utils.transformators import create_column_transformator


@task()
def get_data(data_name: str) -> pd.DataFrame:
    s3_bucket_url = os.getenv('S3_BUCKET_URL', 'http://localhost:4566')
    return pd.read_csv(os.path.join(s3_bucket_url, f'heart-stroke-data/{data_name}'), index_col="id")


# @task()
def train_model_using_hyperopt():
    pass


def pipeline_fit_transformation(data: pd.DataFrame) -> tuple[pd.DataFrame, Pipeline]:
    _transformation_pipeline = create_column_transformator()
    return _transformation_pipeline.fit_transform(data), _transformation_pipeline


@task()
def pipeline_transform(fitted_pipeline: Pipeline, data: pd.DataFrame) -> pd.DataFrame:
    return fitted_pipeline.transform(data)


# @task()
def quickly_perform_grid_search_cv():
    pass


def pickling_obj(obj: Any) -> str:
    dir_path = tempfile.mkdtemp()
    with open(os.path.join(dir_path, 'preprocess_pipeline.pkl'), 'wb') as f_out:
        pickle.dump(obj, f_out)

    return dir_path


@task(log_prints=True)
def train_model(params: dict, data: pd.DataFrame,
                experiment_name: str, tracking_server_host: str) -> str:
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
        final_pipeline = Pipeline([('transformation_pipeline', transformation_pipeline), ('model', model_to_fit)])

        conda_env = mlflow.sklearn.get_default_conda_env()
        conda_env["dependencies"] = [f'lightgbm=={lightgbm.__version__}'] + conda_env["dependencies"]
        recall_1, precision_1, recall_0, precision_0 = calculate_metrics_for_classifier(model_to_fit, feature_data,
                                                                                        target_variable)
        mlflow.log_metric('recall_1', recall_1)
        mlflow.log_metric('precision_1', precision_1)
        mlflow.log_metric('recall_0', recall_0)
        mlflow.log_metric('precision_0', precision_0)
        mlflow.sklearn.log_model(final_pipeline, 'model', registered_model_name="HeartStroke",
                                 conda_env=conda_env, code_paths=['..'])
        print('Model has been logged')
    shutil.rmtree(temp_dir_path)
    return run_id


@task()
def register_model(run_id: str, tracking_server_host: str, model_name: str) -> str:
    mlflow.set_tracking_uri(tracking_server_host)
    model_version = mlflow.register_model(
        model_uri=f"runs:/{run_id}/models",
        name=model_name
    ).version
    return model_version


@flow(name="TrainInitialModel")
def train_initial_model():
    data = get_data('healthcare-dataset-stroke-data.csv')
    _initial_parameters = {'boosting_type': 'gbdt',
                           'class_weight': 'balanced',
                           'colsample_bytree': 1.0,
                           'importance_type': 'split',
                           'learning_rate': 0.01,
                           'max_depth': 10,
                           'min_child_samples': 10,
                           'min_child_weight': 0.001,
                           'min_split_gain': 0.0,
                           'n_estimators': 200,
                           'n_jobs': -1,
                           'num_leaves': 140,
                           'objective': None,
                           'random_state': 42,
                           'reg_alpha': 20,
                           'reg_lambda': 1,
                           'subsample': 0.7,
                           'subsample_for_bin': 200000,
                           'subsample_freq': 10}
    _experiment_name = 'Heart Stroke'
    _tracking_server_host = os.getenv('MLFLOW_HOST', 'http://0.0.0.0:5000')
    run_id = train_model(_initial_parameters, data, _experiment_name, _tracking_server_host)
    client = MlflowClient(_tracking_server_host)
    model_version = register_model(run_id, _tracking_server_host, 'HeartStroke')
    client.transition_model_version_stage(
        name="HeartStroke", version=model_version, stage="Production"
    )

    # @flow()


def retrain_model_using_new_data(path_to_new_data: pd.DataFrame) -> None:
    return None


if __name__ == '__main__':
    train_initial_model()
