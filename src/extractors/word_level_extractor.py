from core.td_data_dict import TD_Data_Dictionary


def filter_words(data: TD_Data_Dictionary):
    keys = data.get_all_keys_pressed()
    for index, key in enumerate(keys):
        if key.casefold() == "Key.ctrl" or key.casefold() == "'Key.ctrl'":
            filtered = drop_to_index(keys, index)
            return filtered


def split_into_words(data):
    words = []
    begin = 0
    for i, j in enumerate(data):
        if j == "Key.space" or j == "'Key.space'":
            words.append(data[begin:i])
            begin = i
    return words


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
        return split_into_words(filter_words(data_dict))
