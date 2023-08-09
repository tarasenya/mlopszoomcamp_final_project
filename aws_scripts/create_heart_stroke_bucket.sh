#!/bin/bash
awslocal s3 mb s3://heart-stroke-data
awslocal s3 mb s3://mlflow-artifacts
awslocal s3 mb s3://evidently-reports