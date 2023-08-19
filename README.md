mlopszoomcamp_finalproject
==============================

This a final project for MLOps Zoomcamp Course.
The aim is to build an automatic pipeline for building, deploying a model to predict a heart stroke
of a patient.
The model is built using heart stroke data from
here: https://www.kaggle.com/datasets/fedesoriano/stroke-prediction-dataset.

Dataset description
-------------------
For a patient X the following information is known (names of the corresponding variables are
self-explanatory):

* gender
* age
* hypertension
* heart_disease
* ever_married
* work_type
* Residence_type
* avg_glucose_level
* bmi
* smoking_status
* stroke.

Problem setting
---------------
In this dataset we choose **stroke** (variable that indicates, whether a patient had a heart stroke)
as a **target variable** and use the above variables as feature variables to predict it.
So we are interested in a binary classification problem. Since we want to determine as many as
possible patients that will likely have a heart attack the metrics we want to optimize is recall.
At the same time the classificator ought to have at least 15% of precision o avoid a trivial
classificator. In this case we sacrifice precision to get a larger recall in a recall-precision
trade-off.

Technical implementation
------------------------
Using the classificator we build a Web Service with an endpoint to predict whether a new patient
with known data will possibly have a heart attack.

Summary
-------
Using gender, age , hypertension , heart_disease, ever_married , work_type, residence_type,
avg_glucose_level, bmi, smoking_status predict whether a patient gets heart stroke. The
classificator should have large recall and reasonable precision, moreover it should be served as
Flask Web application.

**DISCLAIMER:**  I am not a doctor to qualitatively evaluate a model.

**DISCLAIMER 2:** Even if a classificator has a small precision, it can be rather useful. Indeed, if a "reasonable" classificator says that a patient will have a heart stroke, it means that he/she probably resembles the ones that had a heart stroke, so perhaps one should more closely look at him and perform additional medicine procedures.


Project Organization
------------

    ├── Makefile                <- Makefile with commands.
    ├── README.md               <- The top-level README.
    ├── pyproject.toml          <- toml file with project tools requirements.
    ├── prefect.yaml            <- Prefect deployment settings.
    ├── Pipfile                 <- project libraries requirements.
    ├── Pipfile.lock            <- file that defines dependency tree.
    ├── docker-compose.yaml     <- configuration file for docker compose that defines all the services.
    ├── .pre-commit-config.yaml <- pre commit hooks configuration.
    ├── .env                    <- files with environmental variables.
    ├── tests
    │   ├── integratioon_tests <- Tests related to a general integration tests.
    │   ├── unittests          <- Unittests.
    ├── data
    │   ├── interim            <- Intermediate data that has been transformed.
    │   └── raw                <- The original, immutable data dump.
    │
    ├── models                       <- model summaries
    │
    ├── notebooks                    <- Jupyter notebooks for initial working with data
    │
    ├── references                   <- Deployment instructions, manuals and all other explanatory materials.
    │
    ├── src                          <- Source code for use in this project.
    │   ├── __init__.py              <- Makes src a Python module
    │   ├── flows                    <- Scripts dealting with prefect flows
    │   │   └── model_prefomance_flow.py        <- contains flow and tasks that generates evidently reports for a model
    │   │   └── model_training_flows.py         <- contains flow and tasks that execute (re)training of models
    │   │   └── flows_orchestration_scripts.sh  <- bash scirpt for deployment and execution of prefect flows used in docker.
    │   │
    │   ├── utils                                     <- contains useful util scripts
    │   │
    │   ├── web_service                               <- Scripts to train models and then use trained models to make.
    │   │   └──prediction_web_service.py <- flask web app to serve a prediction model.
    ├── dockerized_service_definitions                <- contains Dockerfile for different services
    │   ├── mlflow_service                            <- contains Dockerfile for mlflow server
    │   ├── prefect_development_environment           <- contains Dockerfile for prefect development environment
    │   ├── prefect_execution_environment             <- contains Dockerfile for prefect execution environment
    ├── aws_scripts                                   <- scripts dealing with deployment to aws.

--------

<p><small>Project based on the <a target="_blank" href="https://drivendata.github.io/cookiecutter-data-science/">cookiecutter data science project template</a>. #cookiecutterdatascience</small></p>
