"""
Tests for calculate_metrics_for_classifier
"""
from unittest.mock import patch

from sklearn.dummy import DummyClassifier

from src.utils.metrics import calculate_metrics_for_classifier


def test_calculate_metrics_for_classifier():
    """
    Check whether the output of 'calculate_metrics_for_classifier' is OK at least for
    DummyClassifier (acting as a Mock).
    """
    X = [[1], [2], [3]]
    y = [0, 1, 0]
    clf = DummyClassifier()
    clf.fit(X, y)
    recall_1, precision_1, recall_0, precision_0 = calculate_metrics_for_classifier(
        clf, X, y
    )
    assert recall_1 == 0
    assert precision_1 == 0
    assert recall_0 == 1
    assert precision_0 == 2 / 3


@patch('src.utils.metrics.classification_report')
@patch('src.utils.metrics.confusion_matrix')
def test_calculate_metrics_for_classifier_func_were_called(
    mock_confusion_matrix, mock_classification_report
):
    """
    Check whether necessary functions are called
    """
    X = [[1], [2], [3]]
    y = [0, 1, 0]
    clf = DummyClassifier()
    clf.fit(X, y)
    calculate_metrics_for_classifier(clf, X, y)
    assert mock_confusion_matrix.call_count == 1
    assert mock_classification_report.call_count == 1
