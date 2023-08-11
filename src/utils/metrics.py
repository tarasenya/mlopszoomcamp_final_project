"""
Module to store classification metrics.
"""
from sklearn.metrics import (
    recall_score,
    accuracy_score,
    precision_score,
    confusion_matrix,
    classification_report,
    balanced_accuracy_score,
)


def calculate_metrics_for_classifier(clf, X, y) -> tuple[float, float, float, float]:
    """
    Calculate classification metrics for a classifier, return recalls and precisions for labels.
    printing some of them
    :X: matrix or DataFrame of features
    :y: list of classes
    :return: recall and precisions of positive and negative classes.
    """

    y_predicted = clf.predict(X)

    recall_1: float = recall_score(y, y_predicted, pos_label=1)
    precision_1: float = precision_score(y, y_predicted, pos_label=1)
    recall_0: float = recall_score(y, y_predicted, pos_label=0)
    precision_0: float = precision_score(y, y_predicted, pos_label=0)
    accuracy = accuracy_score(y_predicted, y)
    balanced_accuracy = balanced_accuracy_score(y_predicted, y)
    print(f'Recall_1 {recall_1}, precision_1 {precision_1}')
    print(f'accuracy {accuracy}, balanced_accuracy {balanced_accuracy}')
    print(f'Recall_0 {recall_1}, precision_0 {precision_1}')
    print(confusion_matrix(y, y_predicted))
    print(classification_report(y, y_predicted))
    return recall_1, precision_1, recall_0, precision_0
