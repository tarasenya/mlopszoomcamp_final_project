#!/bin/bash
cd ../..

docker build -t heart-stroke-prediction-service:v1 -f dockerized_service_definitions/web_service/Dockerfile .