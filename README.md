mlopszoomcamp_finalproject
==============================

This a final project for MLOps Zoomcamp Course.
The aim is to build an automatic pipeline for building, deploying a model to predict a heart stroke of a patient.
The model is built using heart stroke data from here: https://www.kaggle.com/datasets/fedesoriano/stroke-prediction-dataset.

Dataset description
-------------------
For a patient X the following information is known (names of the corresponding variables are self-explanatory):
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
In this dataset we choose **stroke** (variable that indicates, whether a patient had a heart stroke) as a **target variable** and use the above variables as feature variables to predict it.
So we are interested in a binary classification problem. Since we want to determine as many as possible patients that will likely have a heart attack the metrics we want to optimize is recall.
At the same time the classificator ought to have at least 15% of precision o avoid a trivial classificator. In this case we sacrifice precision to get a larger recall in a recall-precision trade-off.

Technical implementation
------------------------
Using the classificator we build a Web Service with an endpoint to predict whether a new patient with known data will possibly have a heart attack.

Summary
-------
Using gender, age , hypertension , heart_disease, ever_married , work_type, residence_type, avg_glucose_level, bmi, smoking_status predict whether a patient gets heart stroke. The classificator should have large recall and reasonable precision, moreover it should be served as Flask Web application.

**DISCLAIMER:**  I am not a doctor to qualitatively evaluate a model.

**DISCLAIMER 2:** Even if a classificator has a small precision, it can be rather useful. Indeed, if a "reasonable"
classificator says that a patient will have a heart stroke, it means that he/she probably resembles the ones that had a heart stroke, so perhaps one should more closely look at him and perform additional medicine procedures.


Project Organization
------------

    ├── Makefile           <- Makefile with commands like `make data` or `make train`
    ├── README.md          <- The top-level README for developers using this project.
    ├── data
    │   ├── external       <- Data from third party sources.
    │   ├── interim        <- Intermediate data that has been transformed.
    │   ├── processed      <- The final, canonical data sets for modeling.
    │   └── raw            <- The original, immutable data dump.
    │
    ├── models             <- Trained and serialized models, model predictions, or model summaries
    │
    ├── notebooks          <- Jupyter notebooks. Naming convention is a number (for ordering),
    │                         the creator's initials, and a short `-` delimited description, e.g.
    │                         `1.0-jqp-initial-data-exploration`.
    │
    ├── references         <- Data dictionaries, manuals, and all other explanatory materials.
    │
    ├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
    │   └── figures        <- Generated graphics and figures to be used in reporting
    │
    ├── Pipfile            <-
    ├── Pipfile.loc        <- The requirements file with version for reproducing the analysis environment
    ├── src                <- Source code for use in this project.
    │   ├── __init__.py    <- Makes src a Python module
    │   │
    │   ├── data           <- Scripts to download or generate data
    │   │   └── make_dataset.py
    │   │
    │   ├── features       <- Scripts to turn raw data into features for modeling
    │   │   └── build_features.py
    │   │
    │   ├── models         <- Scripts to train models and then use trained models to make
    │   │   │                 predictions
    │   │   ├── predict_model.py
    │   │   └── train_model.py
    │   │
    │   └── visualization  <- Scripts to create exploratory and results oriented visualizations
    │       └── visualize.py
    │
    └── pyproject.tom            <- toml file to manage python projects


--------

<p><small>Project based on the <a target="_blank" href="https://drivendata.github.io/cookiecutter-data-science/">cookiecutter data science project template</a>. #cookiecutterdatascience</small></p>
