#!/bin/bash
cd ../..

docker build -t mlflow_service:v1 -f dockerized_service_definitions/mlflow_service/Dockerfile .