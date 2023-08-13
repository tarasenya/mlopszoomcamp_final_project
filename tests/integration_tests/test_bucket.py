"""
Easy test to verify if the S3 bucket could be accessed and all three necessary buckets are present
"""
import os

import boto3
import requests

S3_URL = os.getenv('S3_URL', 'http://localhost:4566')


def test_s3_access():
    """
    Testing if S3 bucket could be accessed
    """
    health_endpoint = f'{S3_URL}/health'
    response = requests.get(health_endpoint, timeout=5)
    assert response.json()['services']['s3'] == 'running'


def test_s3_buckets():
    """
    Testing if our s3 contains all necessary buckets
    """
    s3 = boto3.resource('s3', endpoint_url=S3_URL)
    buckets = {bucket.name for bucket in s3.buckets.all()}
    expected_buckets = {'heart-stroke-data', 'mlflow-artifacts', 'evidently-reports'}
    assert buckets == expected_buckets


if __name__ == '__main__':
    test_s3_access()
    test_s3_buckets()
