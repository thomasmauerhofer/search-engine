import numpy as np


def mean(values, ignore_zeros=False):
    used_values = [x for x in values if not ignore_zeros or (ignore_zeros and x != 0)]
    return np.mean(used_values) if len(used_values) else 0
