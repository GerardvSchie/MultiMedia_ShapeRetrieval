import numpy as np


def read_np_array(array_str: str) -> np.array:
    if type(array_str) is np.ndarray:
        return array_str
    # Contains strings
    if array_str.__contains__("'"):
        arr = array_str[2:-2].split("\' \'")
        return np.array(arr)
    # Just an int array
    else:
        array_str = array_str.strip()
        arr = array_str[1:-1].strip().split()
        return np.array(arr, dtype=float)


CATEGORIES = [
    'Airplane',
    'Ant',
    'Armadillo',
    'Bearing',
    'Bird',
    'Bust',
    'Chair',
    'Cup',
    'Fish',
    'FourLeg',
    'Glasses',
    'Hand',
    'Human',
    'Mech',
    'Octopus',
    'Plier',
    'Table',
    'Teddy',
    'Vase'
]


CATEGORY = {
    'Airplane': 0,
    'Ant': 1,
    'Armadillo': 2,
    'Bearing': 3,
    'Bird': 4,
    'Bust': 5,
    'Chair': 6,
    'Cup': 7,
    'Fish': 8,
    'FourLeg': 9,
    'Glasses': 10,
    'Hand': 11,
    'Human': 12,
    'Mech': 13,
    'Octopus': 14,
    'Plier': 15,
    'Table': 16,
    'Teddy': 17,
    'Vase': 18
}

INDEX = {
    0: 'Airplane',
    1: 'Ant',
    2: 'Armadillo',
    3: 'Bearing',
    4: 'Bird',
    5: 'Bust',
    6: 'Chair',
    7: 'Cup',
    8: 'Fish',
    9: 'FourLeg',
    10: 'Glasses',
    11: 'Hand',
    12: 'Human',
    13: 'Mech',
    14: 'Octopus',
    15: 'Plier',
    16: 'Table',
    17: 'Teddy',
    18: 'Vase',
}
