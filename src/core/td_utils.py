# Copyright 2022, Alvin Kuruvilla <alvineasokuruvilla@gmail.com>

# Use of this source code is governed by an MIT-style
# license that can be found in the LICENSE file or at
# https://opensource.org/licenses/MIT.

from converters.pickle_driver import PickleDriver
from core.td_data_dict import TD_Data_Dictionary
import pandas as pd
from typing import List
from rich.traceback import install
import itertools
import copy

install()

#! I think this is the origin of the bad performance as a whole. We need to figure out a way to improve this function and the calculate_key_hold_time since that is the function be called inside of it
#! Perhaps we can look into caching the result of calculate_key_hold_time
def find_matching_keys(template_file_path: str, verification_file_path: str) -> list:
    matches = []
    template_dict = TD_Data_Dictionary(template_file_path)
    verification_dict = TD_Data_Dictionary(verification_file_path)
    template_data = template_dict.calculate_key_hold_time()
    verification_data = verification_dict.calculate_key_hold_time()
    template_keys = template_data.keys()
    verification_keys = verification_data.keys()
    for key in template_keys:
        if key in verification_keys:
            matches.append(key)
    return matches


def is_between(comp, start, end):
    if start <= comp and comp <= end:
        return True
    else:
        return False


def find_matching_interval_keys(
    template_file_path: str, verification_file_path: str
) -> list:
    matches = []
    template_dict = TD_Data_Dictionary(template_file_path)
    verification_dict = TD_Data_Dictionary(verification_file_path)
    template_pairs = template_dict.get_key_pairs()
    verification_pairs = verification_dict.get_key_pairs()
    template_data = template_dict.calculate_key_interval_time(template_pairs)
    verification_data = verification_dict.calculate_key_interval_time(
        verification_pairs
    )
    template_keys = template_data.keys()
    verification_keys = verification_data.keys()
    for key in template_keys:
        if key in verification_keys:
            matches.append(key)
    return matches


def dataframe_from_list(data: list, column_name: List[str]):
    df = pd.DataFrame(data, columns=column_name)
    return df


def compress_interval(intervals_list: List[List[str]]):
    compress = []
    for element in intervals_list:
        assert len(element) == 2
        for i in element:
            if not i in compress:
                compress.append(i)
    return compress


def count_key_matches(template_file_path: str, verification_file_path: str) -> int:
    return len(find_matching_keys(template_file_path, verification_file_path))


def count_interval_key_matches(
    template_file_path: str, verification_file_path: str
) -> int:
    return len(find_matching_interval_keys(template_file_path, verification_file_path))


def find_matching_keys_from_dicts(template_data, verification_data):
    """
    The parameter dictionairs are just normal dicts
    The dictionaries this method takes as parameters are assumed to be ones containing
    the KIT and KHT values to avoid on the fly computation"""
    matches = []
    template_keys = template_data.keys()
    verification_keys = verification_data.keys()
    for key in template_keys:
        if key in verification_keys:
            matches.append(key)
    return matches


def count_key_matches_from_dicts(template_data, verification_data):
    return len(find_matching_keys_from_dicts(template_data, verification_data))


def read_matching_keys_from_files(template_path, verification_path):
    driver = PickleDriver()
    matches = []
    template_dict = driver.load_as_dictionary(template_path)
    verification_dict = driver.load_as_dictionary(verification_path)
    template_keys = template_dict.keys()
    verification_keys = verification_dict.keys()
    for key in template_keys:
        if key in verification_keys:
            matches.append(key)
    return matches


def flatten(lst):
    return list(itertools.chain(*lst))


def merge_sublists(lst):
    return list(itertools.chain.from_iterable(lst))


# FIXME: The method seems to work and gets both the sets of data, but it doesn't seem to retain one set or the other.
# I suspect that this is because dictionaries don't support duplicate keys
def split_dictionary_by_key(dictionary: TD_Data_Dictionary, key):
    res = []
    d = {}
    for k, v in dictionary.data().items():
        if k.get_key_name().lower() == key:
            store = copy.deepcopy(d)
            res.append(store)
            print("Result", res)
            d.clear()
        else:
            d[k.get_key_name()] = v.get_time()
    return res
