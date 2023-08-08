#!/bin/bash
docker run -it --rm -p 9696:9696 -e MLFLOW_HOST='http://172.17.0.1' heart-stroke-prediction-service:v1
