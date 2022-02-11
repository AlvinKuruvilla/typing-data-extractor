from td_data_dict import TD_Data_Dictionary
import pickle

# TODO: For some of these fucntions we should only open file if the file exists to begin with
class PickleDriver:
    def __init__(self):
        pass

    def write_dictionary_to_file(self, data, filepath: str):
        with open(filepath, "ab") as handle:
            pickle.dump(data, handle, protocol=pickle.HIGHEST_PROTOCOL)

    def write_td_data_to_file(self, data: TD_Data_Dictionary, filepath: str):
        """This function will automatically write both the kht and kit dictionaries to the pickle file.
        If you don't want to write both call write_dictionary_to_file()'"""
        with open(filepath, "ab") as handle:
            pickle.dump(
                data.make_kht_dictionary(), handle, protocol=pickle.HIGHEST_PROTOCOL
            )
            pickle.dump(
                data.make_kit_dictionary(), handle, protocol=pickle.HIGHEST_PROTOCOL
            )

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
