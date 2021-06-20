import numpy as np

from src import config


def get_bytes(msg: str) -> list:
    """
    Returns a list of strings. Each string represents a character as a byte.
    :param msg: Original message to transform.
    :return: List of strings.
    """
    return [
        bin(byte)[2:].zfill(config.BITS_X_CHAR)
        for byte in bytearray(msg, 'utf-8')
    ]


def get_filter(bin_str: str) -> np.ndarray:
    """
    Returns a filter to know which pixel has to be odd (0) or even (1).
    :param bin_str: Binary string.
    :return: NumPy array of lists of three binary integers (0 or 1).
    """
    return np.array(
        [list(bin_str[i:i+3]) for i in range(0, len(bin_str), 3)],
        dtype=int
    )


def apply_filter(arr: np.ndarray, arr_filter: np.ndarray) -> None:
    """
    Apply a NumPy array to another NumPy array to (+/-)1 to each element.
    :param bin_str: Original NumPy array with numeric data.
    :param bin_str: NumPy array fixed by binary filter.
    """
    arr[arr % 2 == arr_filter] += 1
