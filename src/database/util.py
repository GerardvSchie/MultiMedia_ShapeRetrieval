import numpy as np


def read_np_array(array_str: str) -> np.array:
    # Contains strings
    if array_str.__contains__("'"):
        arr = array_str[2:-2].split("\' \'")
        return np.array(arr)
    # Just an int array
    else:
        array_str = array_str.strip()
        arr = array_str[1:-1].strip().split()
        return np.array(arr, dtype=float)
