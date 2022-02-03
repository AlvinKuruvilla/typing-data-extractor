# Copyright 2022, Alvin Kuruvilla <alvineasokuruvilla@gmail.com>

# Use of this source code is governed by an MIT-style
# license that can be found in the LICENSE file or at
# https://opensource.org/licenses/MIT.

import os
from log import Logger
from typing import List


def is_csv_file(path: str):
    log = Logger()
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


def chunks(lst, n):
    """Yield a list of n-sized chunks from lst."""
    final = [lst[i * n : (i + 1) * n] for i in range((len(lst) + n - 1) // n)]
    return final


def pretty_print(dictionary):
    for a, b in dictionary.items():
        print(a, b)


def pair_subtract(lst):
    assert len(lst) == 2
    return lst[1] - lst[0]


def n_subtract(*args):
    sub_res = []
    for i in args:
        sub_res.append(pair_subtract(i))
    return sub_res


def m_average(*args):
    """Calculate a running average of a list of lists"""
    s = 0
    for element in args:
        s += element[0] + element[1]
    return s / 2


def running_avg(lst):
    """Calculate a running average of a list"""
    avg = 0
    l = len(lst)
    for element in lst:
        avg += element
    return avg / l


def is_float(n: str):
    try:
        float(n)
        return True
    except ValueError:
        return False


def verify_file_exists(filename: str, extensions: List[str]):
    filename, file_extension = os.path.splitext(filename)
    if file_extension in extensions:
        return True
    else:
        return False
