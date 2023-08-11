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
