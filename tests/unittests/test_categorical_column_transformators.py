"""
Testing CreateCategoricalCutColumnForColumn transformer
"""
import pandas as pd
import pytest

from src.utils.categorical_column_transformators import (
    CreateCategoricalCutColumnForColumn,
)


def test_create_categorical_cut():
    """
    Testing case when the order of terms in a column is sorted
    """
    test_df = pd.DataFrame({'a': [1, 2, 3, 4, 5], 'b': [1, 2, 6, 8, 9]})
    cat_cut_column = CreateCategoricalCutColumnForColumn(
        column_name='b', cut_list=[0, 5, 10]
    )
    result_df = cat_cut_column.fit_transform(test_df)
    expected_df = pd.DataFrame({'a': [1, 2, 3, 4, 5], 'b_cat': [0, 0, 1, 1, 1]})
    assert result_df.equals(expected_df)


def test_create_categorical_cut_mixed_order():
    """
    Testing for the case when cuts are done for the column with mixed order of terms
    """
    test_df = pd.DataFrame({'a': [1, 2, 3, 4, 5], 'b': [1, 6, 7, 2, 9]})
    cat_cut_column = CreateCategoricalCutColumnForColumn(
        column_name='b', cut_list=[0, 5, 10]
    )
    result_df = cat_cut_column.fit_transform(test_df)
    expected_df = pd.DataFrame({'a': [1, 2, 3, 4, 5], 'b_cat': [0, 1, 1, 0, 1]})
    assert result_df.equals(expected_df)


def test_create_categorical_cut_one_bin():
    """
    Testing for the case when cuts are done for one large bin
    """
    test_df = pd.DataFrame({'a': [1, 2, 3, 4, 5], 'b': [1, 6, 7, 2, 9]})
    cat_cut_column = CreateCategoricalCutColumnForColumn(
        column_name='b', cut_list=[0, 10]
    )
    result_df = cat_cut_column.fit_transform(test_df)
    expected_df = pd.DataFrame({'a': [1, 2, 3, 4, 5], 'b_cat': [0, 0, 0, 0, 0]})
    assert result_df.equals(expected_df)


def test_create_categorical_cut_with_wrong_column():
    """
    Testing for the case when cuts are done for wrong column
    """
    test_df = pd.DataFrame({'a': [1, 2, 3, 4, 5], 'b': [1, 6, 7, 2, 9]})
    cat_cut_column = CreateCategoricalCutColumnForColumn(
        column_name='c', cut_list=[0, 10]
    )
    with pytest.raises(KeyError):
        cat_cut_column.fit_transform(test_df)


def test_create_categorical_cut_wrong_range():
    """
    Testing for the case when cuts are done for wrong interval
    """
    test_df = pd.DataFrame({'a': [1, 2, 3, 4, 5], 'b': [1, 6, 7, 2, 9]})
    cat_cut_column = CreateCategoricalCutColumnForColumn(
        column_name='b', cut_list=[-10, 0]
    )
    result_df = cat_cut_column.fit_transform(test_df)
    if result_df['b_cat'].isna().all():
        assert True
    else:
        assert False
