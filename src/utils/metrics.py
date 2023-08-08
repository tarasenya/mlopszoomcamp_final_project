from sklearn.metrics import recall_score, precision_score, accuracy_score, balanced_accuracy_score, confusion_matrix, \
    classification_report


def calculate_metrics_for_classifier(clf, X, y) -> tuple[float, float, float, float]:
    """
    Calculate metrics for a classifier
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
