.PHONY: clean data lint requirements sync_data_to_s3 sync_data_from_s3

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
	docker build -t prefect_development_environment:v1 -f dockerized_service_definitions/prefect_development_environment/Dockerfile .
build_prefect_execution_docker:
	docker build -t prefect_execution_environment:v1 -f dockerized_service_definitions/prefect_execution_environment/Dockerfile .
build_mlflow_docker:
	docker build -t mlflow_service:v1 -f dockerized_service_definitions/mlflow_service/Dockerfile .
build_web_service_docker:
	docker build -t heart-stroke-prediction-service:v1 -f dockerized_service_definitions/web_service/Dockerfile .

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

#################################################################################
# PROJECT                                                                #
#################################################################################



