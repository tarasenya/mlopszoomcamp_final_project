import os
import tempfile

import mlflow
from evidently.metric_preset import ClassificationPreset
from mlflow import MlflowClient
import pandas as pd
from prefect import task, flow
from datetime import datetime
from evidently.report import Report
from evidently import ColumnMapping
from evidently.metrics import ColumnDriftMetric, DatasetDriftMetric, DatasetMissingValuesMetric
from src.utils.constants import NUM_COLS, CAT_COLS, TARGET, PREDICTION, MODEL_NAME, EVIDENTLY_REPORTS_BUCKET
import boto3

MLFLOW_HOST = os.getenv('MLFLOW_HOST', 'http://0.0.0.0:5000')
S3_BUCKET_URL = os.getenv('S3_BUCKET_URL', 'http://localhost:4566')

COLUMN_MAPPING = ColumnMapping(
    prediction=PREDICTION,
    numerical_features=NUM_COLS,
    categorical_features=CAT_COLS,
    target=TARGET
)

report = Report(metrics=[
    ColumnDriftMetric(column_name=PREDICTION),
    DatasetDriftMetric(),
    DatasetMissingValuesMetric(),
    ClassificationPreset()
])


@task(log_prints=True)
def generate_prediction_column(df: pd.DataFrame) -> pd.DataFrame:
    df_copy = df.copy()
    mlflow.set_tracking_uri(MLFLOW_HOST)
    client = MlflowClient(mlflow.get_tracking_uri())
    run_id = client.get_latest_versions(MODEL_NAME)[0].run_id
    logged_model = f'runs:/{run_id}/model'
    model = mlflow.pyfunc.load_model(logged_model)

    df_copy[PREDICTION] = model.predict(df_copy.drop(columns=[TARGET]))
    print(df_copy.head())
    print(df_copy[PREDICTION].head())
    df_copy[TARGET] = df[TARGET]
    return df_copy


@task()
def save_report(report_to_save: Report, report_name: str) -> None:
    s3 = boto3.resource("s3", endpoint_url=os.getenv('S3_BUCKET_URL'))
    dir_path = tempfile.mkdtemp()
    report_to_save.save_html(os.path.join(dir_path, report_name))
    bucket = s3.Bucket(EVIDENTLY_REPORTS_BUCKET)
    bucket.upload_file(os.path.join(dir_path, report_name), report_name)


@flow(name='GenerateReport')
def generate_report() -> None:
    current_heart_stroke_data = f"heart_stroke_{datetime.today().strftime('%Y-%m-%d')}.csv"
    initial_data = pd.read_csv(os.path.join(S3_BUCKET_URL, 'heart-stroke-data/initial_heart_stroke_data.csv'))
    current_data = pd.read_csv(os.path.join(S3_BUCKET_URL, f'heart-stroke-data/{current_heart_stroke_data}'))

    initial_data.drop(columns=['id'])
    current_data.drop(columns=['id'])

    report.run(reference_data=generate_prediction_column(initial_data),
               current_data=generate_prediction_column(current_data),
               column_mapping=COLUMN_MAPPING)
    save_report(report, f"heart_stroke_report_{datetime.today().strftime('%Y-%m-%d')}.html")


if __name__ == '__main__':
    generate_report()
