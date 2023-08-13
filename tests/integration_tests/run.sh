#!/usr/bin/env bash

if [[ -z "${GITHUB_ACTIONS}" ]]; then
  cd "$(dirname "$0")"
fi

#if [ "${LOCAL_IMAGE_NAME_PREFECT_DEVELOPMENT}" == "" ]; then
#    LOCAL_TAG=`date +"%Y-%m-%d-%H-%M"`
#    export LOCAL_IMAGE_NAME_PREFECT_DEVELOPMENT="stream-model-duration:${LOCAL_TAG}"
#    echo "LOCAL_IMAGE_NAME_PREFECT_DEVELOPMENT is not set, building a new image with tag ${LOCAL_IMAGE_NAME_PREFECT_DEVELOPMEN}"
#    docker build -t ${LOCAL_IMAGE_NAME} ..
#else
#    echo "no need to build image ${LOCAL_IMAGE_NAME}"
#fi
cd ../..
#docker build -t prefect_development_environment:v1 -f dockerized_service_definitions/prefect_development_environment/Dockerfile .
#docker build -t prefect_execution_environment:v1 -f dockerized_service_definitions/prefect_execution_environment/Dockerfile .
#docker build -t mlflow_service:v1 -f dockerized_service_definitions/mlflow_service/Dockerfile .
#docker build -t heart-stroke-prediction-service:v1 -f dockerized_service_definitions/web_service/Dockerfile .

sleep 10
docker-compose up -d
sleep 60
echo "Running prediction test"
pipenv run python tests/integration_tests/test_prediction_web_service.py

ERROR_CODE=$?

if [ ${ERROR_CODE} != 0 ]; then
  docker-compose logs
  docker-compose down
  exit ${ERROR_CODE}
fi

pg_isready --fail -d prefect -h localhost -p 548 -U postgresecho "Services down"
curl http://localhost:5000/api/2.0/mlflow/experiments/search?max_results=2 || exit 1

docker-compose down
