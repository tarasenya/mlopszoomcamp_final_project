import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin
import pandas as pd
from sklearn.preprocessing import FunctionTransformer


class CreateCategoricalCutColumnForColumn(BaseEstimator, TransformerMixin):
    """
    Transformer class to create a categorical column from a given column by binning
    """

    def __init__(self, column_name: str, cut_list: list[float]):
        self.column_name = column_name
        self.cut_list = cut_list

    def fit(self, X=None, y=None):
        return self

    def transform(self, X: pd.DataFrame, y=None):
        _cat_column_name = self.column_name + '_cat'
        _age_cat = pd.cut(X[self.column_name], self.cut_list, labels=False)
        X[_cat_column_name] = _age_cat
        X.drop(columns=[self.column_name], inplace=True)
        return X


def to_category(feature_matrix: np.ndarray, cat_cols: list):
    """
    Define a dtype of pandas dataframe categorical column as category.
    This is needed for LGBMClassifier.
    """
    data_frame = pd.DataFrame(feature_matrix, columns=cat_cols)

    for c in data_frame.columns:
        data_frame[c] = data_frame[c].astype('category')

    return data_frame


def define_category_transformer(cat_cols):
    return FunctionTransformer(to_category, kw_args={'cat_cols': cat_cols})
