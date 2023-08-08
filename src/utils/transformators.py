from copy import copy

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import FunctionTransformer, OrdinalEncoder

from src.models.constants import CAT_COLS, NUM_COLS
from src.utils.categorical_column_transformators import define_category_transformer, CreateCategoricalCutColumnForColumn


def to_data_frame(feature_matrix: np.ndarray, cols: list):
    data_frame = pd.DataFrame(feature_matrix, columns=cols)
    return data_frame


def create_column_transformator() -> Pipeline:
    cat_cols = copy(CAT_COLS)
    num_cols = copy(NUM_COLS)
    cat_cols.append('age_cat')
    num_cols.remove('age')

    imp_mean = SimpleImputer(missing_values=np.nan, strategy='mean')
    imp_mode = SimpleImputer(missing_values=np.nan, strategy='most_frequent')
    to_category_transformer = define_category_transformer(cat_cols)

    num_pipe = Pipeline([('num_imputer', imp_mean),
                         ('to_data_frame', FunctionTransformer(to_data_frame, kw_args={'cols': num_cols}))])
    cat_pipe = Pipeline([('cat_imputer', imp_mode), ('encoder', OrdinalEncoder(dtype=int)),
                         ('to_category', to_category_transformer)])

    ct = ColumnTransformer(
        transformers=[("cat_preprocess", cat_pipe, cat_cols),
                      ("num_preprocess", num_pipe, num_cols)],
        verbose_feature_names_out=False, ).set_output(transform='pandas', )

    _final_pipeline = Pipeline([('create_cat_column', CreateCategoricalCutColumnForColumn('age', [0, 70, 100])),
                                ('column_transformer', ct)])
    return _final_pipeline
