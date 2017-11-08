from keras import backend as k

"""This Code is from https://github.com/fchollet/keras/issues/5400"""


def mcor(y_true, y_pred):
    # matthews_correlation
    y_pred_pos = k.round(k.clip(y_pred, 0, 1))
    y_pred_neg = 1 - y_pred_pos

    y_pos = k.round(k.clip(y_true, 0, 1))
    y_neg = 1 - y_pos

    tp = k.sum(y_pos * y_pred_pos)
    tn = k.sum(y_neg * y_pred_neg)

    fp = k.sum(y_neg * y_pred_pos)
    fn = k.sum(y_pos * y_pred_neg)

    numerator = (tp * tn - fp * fn)
    denominator = k.sqrt((tp + fp) * (tp + fn) * (tn + fp) * (tn + fn))

    return numerator / (denominator + k.epsilon())


def precision(y_true, y_pred):
    """Precision metric.

    Only computes a batch-wise average of precision.

    Computes the precision, a metric for multi-label classification of
    how many selected items are relevant.
    """
    true_positives = k.sum(k.round(k.clip(y_true * y_pred, 0, 1)))
    predicted_positives = k.sum(k.round(k.clip(y_pred, 0, 1)))
    precision = true_positives / (predicted_positives + k.epsilon())
    return precision


def recall(y_true, y_pred):
    """Recall metric.

    Only computes a batch-wise average of recall.

    Computes the recall, a metric for multi-label classification of
    how many relevant items are selected.
    """
    true_positives = k.sum(k.round(k.clip(y_true * y_pred, 0, 1)))
    possible_positives = k.sum(k.round(k.clip(y_true, 0, 1)))
    recall = true_positives / (possible_positives + k.epsilon())
    return recall


def f1(y_true, y_pred):
    def recall_f1(y_true, y_pred):
        """Recall metric.

        Only computes a batch-wise average of recall.

        Computes the recall, a metric for multi-label classification of
        how many relevant items are selected.
        """
        true_positives = k.sum(k.round(k.clip(y_true * y_pred, 0, 1)))
        possible_positives = k.sum(k.round(k.clip(y_true, 0, 1)))
        recall = true_positives / (possible_positives + k.epsilon())
        return recall

    def precision_f1(y_true, y_pred):
        """Precision metric.

        Only computes a batch-wise average of precision.

        Computes the precision, a metric for multi-label classification of
        how many selected items are relevant.
        """
        true_positives = k.sum(k.round(k.clip(y_true * y_pred, 0, 1)))
        predicted_positives = k.sum(k.round(k.clip(y_pred, 0, 1)))
        precision = true_positives / (predicted_positives + k.epsilon())
        return precision

    precision = precision_f1(y_true, y_pred)
    recall = recall_f1(y_true, y_pred)
    return 2 * ((precision * recall) / (precision + recall))
