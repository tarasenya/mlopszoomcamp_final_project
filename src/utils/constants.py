"""
Module to store constants
"""
CAT_COLS = [
    'gender',
    'hypertension',
    'heart_disease',
    'ever_married',
    'work_type',
    'Residence_type',
    'smoking_status',
]
NUM_COLS = ['age', 'avg_glucose_level', 'bmi']
TARGET = 'stroke'
PREDICTION = 'prediction'
MODEL_NAME = 'HeartStroke'
EVIDENTLY_REPORTS_BUCKET = 'evidently-reports'
HEART_STROKE_DATA = 'heart-stroke-data'
EXPERIMENT_NAME = 'Heart Stroke'
INITIAL_PARAMETERS_FOR_LGBM_CLF = {
    'boosting_type': 'gbdt',
    'class_weight': 'balanced',
    'colsample_bytree': 1.0,
    'importance_type': 'split',
    'learning_rate': 0.01,
    'max_depth': 10,
    'min_child_samples': 10,
    'min_child_weight': 0.001,
    'min_split_gain': 0.0,
    'n_estimators': 200,
    'n_jobs': -1,
    'num_leaves': 140,
    'objective': None,
    'random_state': 42,
    'reg_alpha': 20,
    'reg_lambda': 1,
    'subsample': 0.7,
    'subsample_for_bin': 200000,
    'subsample_freq': 10,
}
LIGHTGBM_PARAMETERS = {
    'num_leaves': [50, 70, 80, 100, 120, 140, 160],
    'max_depth': [3, 5, 7, 10, 15],
    'learning_rate': [0.001, 0.01, 0.1, 1, 1.5, 2, 2.5],
    'n_estimators': [50, 100, 200, 300, 400, 500, 600],
    'class_weight': [{1: 18}, 'balanced'],
    'min_child_samples': [5, 10, 20, 30, 40, 50, 60, 70, 80, 90],
    'subsample': [1.0, 0.9, 0.7],
    'subsample_freq': [10, 50, 100],
    'reg_alpha': [0.001, 0.01, 0.1, 1, 5, 10, 15, 20],
    'reg_lambda': [0.001, 0.01, 0.1, 1, 5, 10, 20, 25, 30],
}
