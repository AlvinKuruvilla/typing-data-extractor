from utils import (
    is_csv_file,
    pair_subtract,
    pretty_print,
    chunks,
    running_avg,
)
import csv
from typing import List
import collections


class TD_Data_Value:
    def __init__(self, elements: List[str]):
        self.elements = elements

    def get_action(self):
        return self.elements[0]

    def get_time(self):
        return self.elements[1]


class TD_Data_Key:
    def __init__(self, key_name: str):
        self.key_name = key_name

    def get_key_name(self):
        return self.key_name


class TD_Data_Dictionary:
    def __init__(self, csv_data_path: str) -> None:
        self.csv_data_path = csv_data_path
        is_csv_file(self.csv_data_path)
        self.data_dict = {}
        is_csv_file(self.csv_data_path)
        with open(self.csv_data_path, "r") as file:
            reader = csv.reader(file)
            # Skip the header and move the reader forward to next line
            _ = next(reader)
            for i, line in enumerate(reader):
                self.data_dict[TD_Data_Key(line[1])] = TD_Data_Value([line[0], line[2]])
                # print("line[{}] = {}".format(i, line))
            # for k, v in self.data_dict.items():
            #     print(k.get_key_name(), v.get_action(), v.get_time(), end=" \n")

    def get_all_keys_pressed(self):
        """This gets every key pressed including repeats and keys that may have been pressed but not released for some reason. This will also remove instances of \x03 (ctrl+c)"""
        res = []
        for k, _ in self.data_dict.items():
            if k.get_key_name() != "'\\x03'":
                res.append(k.get_key_name())
        return res

    def get_unique_keys(self):
        res = self.get_all_keys_pressed()
        for key in res:
            if res.count(key) % 2 != 0:
                res.remove(key)
        unique = []
        for k in res:
            if not k in unique:
                unique.append(k)
        return unique

    def get_key_pairs(self):
        unique = self.get_unique_keys()
        pairs = []
        i = 0
        while i < len(unique):
            if i + 1 == len(unique):
                return pairs
            pairs.append([unique[i], unique[i + 1]])
            i += 1

    def calculate_key_hit_time(self):
        keys = self.get_unique_keys()
        store = collections.defaultdict(list)
        final = collections.defaultdict(float)
        res = collections.defaultdict(list)
        for key in keys:
            for i, j in self.data_dict.items():
                if key == i.get_key_name():
                    store[i] = j.get_time()
        for a, b in store.items():
            # print(a.get_key_name(), b)
            res[a.get_key_name()].append(b)
            # So at this point we should have a dictionary called 'res' whose
            # keys are the unique keys pressed and whose values are a list
            # containing the sequential press and release times.
            # Now all we have to do is if the values array has 2 entries we can
            # just subtract them to find the key hit time for that key. If it
            # has a multiple of 2 number of entries we have to split the array
            # into groups of 2 elements, find the difference between the groups
            # and finally average their differences together
        # pretty_print(res)
        for x, y in res.items():
            if len(y) == 2:
                floats = [float(item) for item in y]
                subtr = floats[1] - floats[0]
                final[x] = subtr
                # print("Top if:", x, subtr)
            elif len(y) % 2 == 0 and len(y) != 2:
                subtraction_holder = []
                multi_floats = [float(item) for item in y]
                multi_diff = chunks(multi_floats, 2)
                for diff in multi_diff:
                    subtraction_holder.append(pair_subtract(diff))
                multi_avg = running_avg(subtraction_holder)
                final[x] = multi_avg
                # print("In elif:", x, multi_avg)
        pretty_print(final)
        return final
