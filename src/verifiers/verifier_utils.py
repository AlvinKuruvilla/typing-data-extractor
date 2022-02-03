# Copyright 2022, Alvin Kuruvilla <alvineasokuruvilla@gmail.com>

# Use of this source code is governed by an MIT-style
# license that can be found in the LICENSE file or at
# https://opensource.org/licenses/MIT.

from td_data_dict import TD_Data_Dictionary
import pandas as pd
from typing import List


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


#! TODO: When creating a dataframe the list generated from this function dataframe_from_list(), expects a list
#! with 2 elements for column names when it should only need a single column
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
