# Copyright 2022, Alvin Kuruvilla <alvineasokuruvilla@gmail.com>

# Use of this source code is governed by an MIT-style
# license that can be found in the LICENSE file or at
# https://opensource.org/licenses/MIT.

import os
from core.td_data_dict import TD_Data_Dictionary


def test_path():
    path = os.path.join(os.getcwd(), "Test", "sources", "single-entry-template.csv")
    holder = TD_Data_Dictionary(path)
    assert holder.path() == path


def test_get_data_dictionary():
    path = os.path.join(os.getcwd(), "Test", "sources", "single-entry-template.csv")
    holder = TD_Data_Dictionary(path)
    assert len(holder.data()) == 9


def test_get_all_keys_pressed():
    path = os.path.join(os.getcwd(), "Test", "sources", "single-entry-template.csv")
    holder = TD_Data_Dictionary(path)
    assert len(holder.get_all_keys_pressed()) == 9


def test_get_unique_keys():
    path = os.path.join(os.getcwd(), "Test", "sources", "single-entry-template.csv")
    holder = TD_Data_Dictionary(path)
    assert len(holder.get_unique_keys()) == 4


def test_get_key_pairs():
    # This is test code we can look at to see if the pairs are correct
    # d1 = TD_Data_Dictionary(
    #   os.path.join(os.getcwd(), "Test", "sources", "single-entry-template.csv")
    # )
    # print(d1.get_key_pairs())
    # print(len(d1.get_key_pairs())) -> should return 8 in this case
    path = os.path.join(os.getcwd(), "Test", "sources", "single-entry-template.csv")
    holder = TD_Data_Dictionary(path)
    assert len(holder.get_key_pairs()) == 8


def test_single_entry_kht_calculation():
    d1 = TD_Data_Dictionary(
        os.path.join(os.getcwd(), "Test", "sources", "single-entry-verification.csv")
    )
    data = d1.calculate_key_hold_time()
    assert len(data) == 1
    assert list(data.values())[0] == 0.13029980659484863
