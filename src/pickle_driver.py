from td_data_dict import TD_Data_Dictionary, KIT_Type
import pickle
from utils import strip_filename
import os

# TODO: For some of these fucntions we should only open file if the file exists to begin with
class PickleDriver:
    def __init__(self):
        pass

    def write_kht_dictionary_to_file(self, data, filepath: str):
        mod_file_name = "KHT_" + strip_filename(filepath)
        with open(filepath, "wb") as handle:
            pickle.dump(data, handle, protocol=pickle.HIGHEST_PROTOCOL)
        os.rename(filepath, mod_file_name)

    def write_kit_dictionary_to_file(self, data, kit_type: KIT_Type, filepath):
        if kit_type == KIT_Type.Press_Press:
            mod_file_name = "KIT_PP_" + strip_filename(filepath)
            with open(filepath, "wb") as handle:
                pickle.dump(data, handle, protocol=pickle.HIGHEST_PROTOCOL)
            os.rename(filepath, mod_file_name)
        elif kit_type == KIT_Type.Press_Release:
            mod_file_name = "KIT_PR_" + strip_filename(filepath)
            with open(filepath, "wb") as handle:
                pickle.dump(data, handle, protocol=pickle.HIGHEST_PROTOCOL)
            os.rename(filepath, mod_file_name)
        elif kit_type == KIT_Type.Release_Press:
            mod_file_name = "KIT_RP_" + strip_filename(filepath)
            with open(filepath, "wb") as handle:
                pickle.dump(data, handle, protocol=pickle.HIGHEST_PROTOCOL)
            os.rename(filepath, mod_file_name)
        elif kit_type == KIT_Type.Release_Release:
            mod_file_name = "KIT_RR_" + strip_filename(filepath)
            with open(filepath, "wb") as handle:
                pickle.dump(data, handle, protocol=pickle.HIGHEST_PROTOCOL)
            os.rename(filepath, mod_file_name)

    def read_to_list(self, filepath):
        objects = []
        with open(filepath, "rb") as pickle_file:
            while True:
                try:
                    objects.append(pickle.load(pickle_file))
                except EOFError:
                    return objects

    def wipe_file(self, filepath: str):
        """Delete the contents of the file at the specified path without deleting it"""
        with open(filepath, "w") as handle:
            handle.truncate()
