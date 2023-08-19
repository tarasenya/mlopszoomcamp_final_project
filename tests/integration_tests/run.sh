#!/usr/bin/env bash

cd ../..
set -a
set -o allexport
. .env
set +a
#docker build -t prefect_development_environment:v1 -f dockerized_service_definitions/prefect_development_environment/Dockerfile .
#docker build -t prefect_execution_environment:v1 -f dockerized_service_definitions/prefect_execution_environment/Dockerfile .
#docker build -t mlflow_service:v1 -f dockerized_service_definitions/mlflow_service/Dockerfile .
#docker build -t heart-stroke-prediction-service:v1 -f dockerized_service_definitions/web_service/Dockerfile .

#sleep 10
#docker-compose up -d
#sleep 60
echo "Running prediction test"
pipenv run python tests/integration_tests/test_prediction_web_service.py

ERROR_CODE=$?

if [ ${ERROR_CODE} != 0 ]; then
  docker-compose logs
  docker-compose down
  exit ${ERROR_CODE}
fi

# Verify if the dedicated postgresql server is up. Commented because pg_isready util should be
# installed on a server/computer to execute it, which is not pre assumed.
# echo "Testing postgresql"
# pg_isready --fail -d prod_db -h localhost -p 5432 -U postgres || exit 1
#if [ ${ERROR_CODE} != 0 ]; then
#  docker-compose logs
#  docker-compose down
#  exit ${ERROR_CODE}
#fi
# Verify if mlflow server is up and the dedicated experiment has been created
echo "Testing mlflow"

curl --fail ${MLFLOW_HOST}:${MLFLOW_PORT}/api/2.0/mlflow/registered-models/get?name=HeartStroke || exit 1
ERROR_CODE=$?
if [ ${ERROR_CODE} != 0 ]; then
  docker-compose logs
  docker-compose down
  exit ${ERROR_CODE}
fi

# Verify if prefect server is up and running
echo "Testing prefect health"
curl --fail ${PREFECT_HOST}:${PREFECT_PORT}/api/health || exit 1

ERROR_CODE=$?
if [ ${ERROR_CODE} != 0 ]; then
  docker-compose logs
  docker-compose down
  exit ${ERROR_CODE}
fi

# Testing S3 Bucket
echo "Testing S3"
pipenv run python tests/integration_tests/test_bucket.py

ERROR_CODE=$?
if [ ${ERROR_CODE} != 0 ]; then
  docker-compose logs
  docker-compose down
  exit ${ERROR_CODE}
fi

echo "Everything was fine. Services need to rest."
docker-compose down
