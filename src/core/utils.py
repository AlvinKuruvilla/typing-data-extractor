# Copyright 2022, Alvin Kuruvilla <alvineasokuruvilla@gmail.com>

# Use of this source code is governed by an MIT-style
# license that can be found in the LICENSE file or at
# https://opensource.org/licenses/MIT.

import os
from core.log import Logger
from typing import List, Any
from numpy import mean


def is_csv_file(path: str) -> bool:
    """
    Check if a provided path is to a CSV file.

    Parameters
    ----------
    path: str
          The path to be checked.
    Returns
    -------
    bool
    """
    log = Logger("is_csv_file")
    is_file = os.path.isfile(path)
    if is_file:
        # Now check that the extension is CSV
        if path.lower().endswith(".csv"):
            return True
        else:
            log.km_fatal(path + ", is not a csv file")
            return False
    else:
        log.km_fatal(path + " , is not a file")
        return False


def chunks(lst: list, n: int) -> list:
    """
    Yield a list of n-sized chunks from a list.

    Parameters
    ----------
    text: str
          The text to be made into a banner.
    Returns
    -------
    None
    """
    final = [lst[i * n : (i + 1) * n] for i in range((len(lst) + n - 1) // n)]
    return final


def pretty_print(dictionary: dict) -> None:
    """
    Pretty print a dictionary.

    Parameters
    ----------
    dictionary: dict
          The dictionary to be pretty printed.
    Returns
    -------
    None
    """
    for a, b in dictionary.items():
        print(a, b)


def pair_subtract(lst: list) -> int:
    """
    Cleanly subtract the elements of a 2 element list.

    Parameters
    ----------
    lst: lst
          The list to subtract elements from.
    Returns
    -------
    int
    """
    assert len(lst) == 2
    return lst[1] - lst[0]


def running_avg(lst: list) -> Any:
    """
    Calculate a running average of a list

    Parameters
    ----------
    lst: lst
          The list to find the average of.
    Returns
    -------
    int
    """
    return mean(lst, dtype=object)


def is_float(n: str) -> bool:
    """
    Checks if a string is a valid float
    Parameters
    ----------
    n: str
          The string to check.
    Returns
    -------
    bool
    """
    try:
        float(n)
        return True
    except ValueError:
        return False


def verify_file_exists(filename: str, extensions: List[str]) -> bool:
    """
    Verify that a file exists at least one of the provided extensions
    Parameters
    ----------
    filename: str
          The filename to check.
    extensions: List[str]
          The possible extensions to use.
    Returns
    -------
    bool
    """
    filename, file_extension = os.path.splitext(filename)
    if file_extension in extensions:
        return True
    else:
        return False


def strip_filename(filepath: str, keep_extension: bool = True):
    """
    Strip a filename from a path with or without its extension
    Parameters
    ----------
    filepath: str
          The filepath to use.
    keep_extension: bool
          Whether or not to keep the extension of the file.
          Defaults to True so the extension will be kept
    Returns
    -------
    Any[several types]
    """
    filename = os.path.basename(filepath)
    if keep_extension:
        return filename
    else:
        return os.path.splitext(filepath)[0]
