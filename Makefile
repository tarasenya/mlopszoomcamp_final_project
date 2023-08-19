.PHONY: clean quality_checks setup

#################################################################################
# GLOBALS                                                                       #
#################################################################################

PROJECT_DIR := $(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))
BUCKET = mlopszoomcamp_taras_data
PROFILE = default
PROJECT_NAME = mlopszoomcamp_finalproject
PYTHON_INTERPRETER = python3

#################################################################################
# COMMANDS                                                                      #
#################################################################################
## Build Docker Container
build_prefect_development_docker:
	docker build -t prefect_development_environment:${DOCKER_IMAGE_TAG} -f dockerized_service_definitions/prefect_development_environment/Dockerfile .
build_prefect_execution_docker:
	docker build -t prefect_execution_environment:${DOCKER_IMAGE_TAG} -f dockerized_service_definitions/prefect_execution_environment/Dockerfile .
build_mlflow_docker:
	docker build -t mlflow_service:${DOCKER_IMAGE_TAG} -f dockerized_service_definitions/mlflow_service/Dockerfile .
build_web_service_docker:
	docker build -t heart-stroke-prediction-service:${DOCKER_IMAGE_TAG} -f dockerized_service_definitions/web_service/Dockerfile .
build_all_services:
	docker build -t mlflow_service:${DOCKER_IMAGE_TAG} -f dockerized_service_definitions/mlflow_service/Dockerfile .
	docker build -t prefect_development_environment:${DOCKER_IMAGE_TAG} -f dockerized_service_definitions/prefect_development_environment/Dockerfile .
	docker build -t prefect_execution_environment:${DOCKER_IMAGE_TAG} -f dockerized_service_definitions/prefect_execution_environment/Dockerfile .
	docker build -t heart-stroke-prediction-service:${DOCKER_IMAGE_TAG} -f dockerized_service_definitions/web_service/Dockerfile .
set_environment_variables:
	set -a
	set -o allexport
	. ${PROJECT_DIR}/.env
	set +a
## Delete all compiled Python files
clean:
	find . -type f -name "*.py[co]" -delete
	find . -type d -name "__pycache__" -delete

## Quality checks
quality_checks:
	isort .
	black .
	pylint --recursive=y .
## Set up python interpreter environment
setup:
	pipenv install --dev
	pre-commit install
