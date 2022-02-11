from td_data_dict import TD_Data_Dictionary
import json

# TODO: For some of these fucntions we should only open file if the file exists to begin with
#! FIXME: THE JSON THIS GENERATES REQUIRES MANUAL EDITING TO BE VALID... WE HAVE TO DO THIS BETTER
class JSONDriver(object):
    def __init__(self):
        pass

    def write_kht_dictionary_to_file(self, data, filepath: str):
        # FIXME: This adds one to many commas to the generated file
        with open(filepath, "a") as handle:
            formatted_data = {}
            for key, value in data.items():
                obj = json.dumps(key)
                formatted_data[obj] = value
            handle.write("{")
            for key, value in formatted_data.items():
                handle.write("%s:%s , \n" % (key, value))
            handle.write("}")

    def write_td_data_to_file(self, data: TD_Data_Dictionary, filepath: str):
        """This function will automatically write both the kht and kit dictionaries to the pickle file.
        If you don't want to write both call write_dictionary_to_file()'"""
        with open(filepath, "a") as handle:
            kit = {}
            kht_id = {
                "ID": "KHT",
            }
            kit_id = {
                "ID": "KIT",
            }
            kht = data.make_kht_dictionary()
            kht.update(kht_id)
            t_kit = data.make_kit_dictionary()
            for key, value in t_kit.items():
                obj = json.dumps(key)
                kit[obj] = value
            kit.update(kit_id)
            json.dump(kht, handle)
            json.dump(kit, handle)

    def write_kit_dictionary_to_file(self, data, filepath: str):
        with open(filepath, "a") as handle:
            formatted_data = {}
            handle.write("{")
            for keyset, value in data.items():
                for key in keyset:
                    obj = json.dumps(key)
                    formatted_data[obj] = value
                    for key, value in formatted_data.items():
                        handle.write("%s:%s , \n" % (key, value))
            handle.write("}")

    def read(self, filepath):
        with open(filepath, "r") as handle:
            data = json.load(handle)
            return data

    def wipe_file(self, filepath: str):
        """Delete the contents of the file at the specified path without deleting it"""
        with open(filepath, "w") as handle:
            handle.truncate()
