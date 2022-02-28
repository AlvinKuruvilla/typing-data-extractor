from core.td_data_dict import TD_Data_Dictionary
from rich.traceback import install
import copy
from itertools import groupby

install()


def filter_words(data: TD_Data_Dictionary):
    """This function removes all instances of Key.ctrl from the list of keys and
    any repeats because of Press and Realese events"""
    # NOTE: We may just want to remove all instances of Key.ctrl from the list and anything that follows that
    keys = data.get_letters()
    return keys


def split_by_space(data):
    return [
        list(group) for k, group in groupby(data, lambda x: x == "key.space") if not k
    ]


def drop(keys, index):
    if index < 0 or index >= len(keys):
        raise IndexError("Provided index is not valid")
    del keys[index]
    return keys


def drop_to_index(data, index: int):
    """This is an inclusive drop operation so the index parameter will also be dropped"""
    if index < 0 or index >= len(data):
        raise IndexError("Provided index is not valid")
    return data[0:index]


class WordExtractor:
    def __init__(
        self, template_dict: TD_Data_Dictionary, verification_dict: TD_Data_Dictionary
    ):
        self.template_dict = template_dict
        self.verification_dict = verification_dict

    def get_template(self):
        return self.template_dict

    def get_verification(self):
        return self.verification_dict

    def set_template(self, new_template: TD_Data_Dictionary):
        self.template_dict = new_template

    def set_verification(self, new_verification: TD_Data_Dictionary):
        self.verification_dict = new_verification

    def get_filtered_keys_list(self, data_dict: TD_Data_Dictionary):
        """This function returns all keys (including repeats) but will filter
        all keys including and after Key.ctrl"""
        return filter_words(data_dict)

    def get_words(self, data_dict: TD_Data_Dictionary):
        items = data_dict.get_letters()
        temp = copy.deepcopy(items)
        words = []
        for i, item in enumerate(items):
            if item.lower() == "key.ctrl":
                clean = drop_to_index(temp, i)
        word_set = split_by_space(clean)
        for letter_set in word_set:
            words.append("".join(letter_set))
        return words
