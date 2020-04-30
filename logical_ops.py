import numpy as np


def logical_or_max(seq):
    # take the max of elems in seq, if all elems are None then return None
    non_null_elems = [elem for elem in seq if elem is not None]
    if len(non_null_elems) > 0:
        return np.max(non_null_elems)
    else:
        return None


def logical_and_min(seq):
    # take the min of all elems in seq, if all elems are None then return None
    non_null_elems = [elem for elem in seq if elem is not None]
    if len(non_null_elems) > 0:
        return np.min(non_null_elems)
    else:
        return None
