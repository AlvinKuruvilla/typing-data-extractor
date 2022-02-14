# Copyright 2022, Alvin Kuruvilla <alvineasokuruvilla@gmail.com>

# Use of this source code is governed by an MIT-style
# license that can be found in the LICENSE file or at
# https://opensource.org/licenses/MIT.


from math import pow
from core.td_data_dict import TD_Data_Dictionary
from core.log import Logger

from verifiers.verifier_utils import find_matching_keys, find_matching_interval_keys

# NOTE: As far as I can tell this verifier operates on the entire set of verification data
# i.e. it considers all the KHT values from the verification data as a whole sample and then compares the whole thing
# to the entire set of template data which is treated similarly
# For our use case we may want to treat each KHT value as its own individual sample and
# then only compare it to the corresponding KHT in the template data.


def dictionary_sort_by_value(d, ascending=True):
    """Performs a sort on a dictionary by value
    Defaults to an ascending sort order
    """
    sorted_dictionary = {}
    if ascending:
        sorted_list = sorted(d.items(), key=lambda x: x[1])
    if ascending == False:
        sorted_list = sorted(d.items(), key=lambda x: x[1], reverse=True)
    for i in sorted_list:
        sorted_dictionary[str(i[0])] = str(i[1])
    return sorted_dictionary


class RelativeVerifier:
    def __init__(
        self, template_file_path: str, verification_file_path: str, threshold: float
    ) -> None:
        self.THRESHOLD = threshold
        self.template_file_path = template_file_path
        self.verification_file_path = verification_file_path
        self.template_td_data_dict = TD_Data_Dictionary(self.template_file_path)
        self.verification_td_data_dict = TD_Data_Dictionary(self.verification_file_path)

    def class_name(self) -> str:
        return "Relative Verifier"

    def degree_of_disorder(self, use_kit=False) -> int:
        # The algorithm to find degree of disorder is as follows:
        # So let's say we have the two tables listed below
        # To find the disorder of table V, in this example it would be the first table, we calculate the
        # difference between the position of an element in V and that same element's position in
        # the ordered table, in this example that is the second table
        # For example, in table V element 'H' is in position 0, and in the ordered table 'H' is in position 1
        # so the degree of disorder for element 'H' is 1
        # Therefore, to calculate the degree of disorder for the entire table V, we calculate the degree of disorder
        # for each element and then sum them together
        # In this example, the degrees of disorder for each element is:
        #   - H: 1
        #   - W: 3
        #   - C: 2
        #   - Q: 0
        #   - M: 2
        #    Table 1: | H | W | C | Q | M |
        #    Table 2: | C | H | M | Q | W |
        # So the degree of disorder for table V is 8

        # NOTE: In our specific use case, I think the first table should be the verification attempt array and
        # the sorted table should be the template array
        # Thus we should iterate every element in the template table and keep a running sum of its distance
        # to the corresponding entry in the verification table using the self.find_distance() function.
        disorder = 0
        if use_kit == False:
            verification_keys = find_matching_keys(
                self.template_file_path, self.verification_file_path
            )
            for entry in verification_keys:
                disorder += self.find_distance(entry)
            return disorder
        else:
            verification_keys = find_matching_interval_keys(
                self.template_file_path, self.verification_file_path
            )
            for entry in verification_keys:
                disorder += self.find_distance(entry, True)
            return disorder

    def absolute_degree_of_disorder(self, use_kit=False) -> float:
        # The formula to calculate the absolute degree of disorder is simply:
        #   1) Find the degree of disorder for the entire table
        #   2) Calculate the maximum degree of disorder for a table with n elements accroding to the formula (n^2 -1)/2
        #   3) Divide the degree of disorder with the maximum calculated in the previous step
        if use_kit == False:
            return self.degree_of_disorder() / self.max_degree_of_disorder()
        else:
            return self.degree_of_disorder(True) / self.max_degree_of_disorder(True)

    def set_threshold(self, threshold):
        self.THRESHOLD = threshold

    def max_degree_of_disorder(self, use_kit=False) -> float:
        # To calculate the maximum degree of disorder for a table with n elements use the formula (n^2 -1)/2
        if use_kit == False:
            verification_hit_dict = self.template_td_data_dict.calculate_key_hold_time()
            n = len(list(verification_hit_dict.keys()))
            return (pow(n, 2) - 1) / 2
        else:
            verification_hit_dict = (
                self.template_td_data_dict.calculate_key_interval_time()
            )
            n = len(list(verification_hit_dict.keys()))
            return (pow(n, 2) - 1) / 2

    def is_key_valid(self, use_kit=False) -> bool:
        # Maybe to see if typing samples are valid we compare the absolute degree of disorder with a given
        # threshold value and if it is less than the threshold the sample is considered valid
        if use_kit == False:
            if self.absolute_degree_of_disorder() < self.THRESHOLD:
                return True
            else:
                return False
        else:
            if self.absolute_degree_of_disorder(True) < self.THRESHOLD:
                return True
            else:
                return False

    def find_distance(self, entry, use_kit=False) -> int:
        # Finds the distance between a given entry from the template table and
        # the corresponding key letter entry in the verification table
        log = Logger("find_distance")
        template_hit_dict = self.template_td_data_dict.calculate_key_hold_time()
        store = dictionary_sort_by_value(template_hit_dict)
        distance = 0
        if use_kit == False:
            verification_keys = find_matching_keys(
                self.template_file_path, self.verification_file_path
            )
        else:
            verification_keys = find_matching_interval_keys(
                self.template_file_path, self.verification_file_path
            )
        sorted_template_keys = list(store.keys())

        if not entry in sorted_template_keys:
            log.km_fatal(
                "Provided entry" + entry + "is not in the list of sorted template keys"
            )
            return
        if not entry in verification_keys:
            log.km_fatal(
                "Provided entry" + entry + "is not in the list of verification keys"
            )
            return
        for cell in verification_keys:
            if cell == entry:
                return distance
            else:
                distance += 1
        return distance

    def template_path(self):
        return self.template_file_path

    def verification_path(self):
        return self.verification_file_path

    def get_threshold(self):
        return self.THRESHOLD

    def find_all_valid_keys(self, use_kit=False):
        valids = []
        if use_kit == False:
            matches = find_matching_keys(
                self.template_file_path, self.verification_file_path
            )

            for key in matches:
                if self.is_key_valid(False):
                    valids.append(key)
            return valids
        else:
            matches = find_matching_interval_keys(
                self.template_file_path, self.verification_file_path
            )
            for key in matches:
                if self.is_key_valid(True):
                    valids.append(key)
            return valids

    # NOTE: We don't _have_ to do the loop because self.absolute_degree_of_disorder() operates on the whole table
    # anyway. So it is okay that each key has the same timing value from the verifiers perspective
    def get_valid_keys_data(self, use_kit=False):
        data = {}
        if use_kit == False:
            matches = find_matching_keys(
                self.template_file_path, self.verification_file_path
            )
            for key in matches:
                if self.absolute_degree_of_disorder() < self.THRESHOLD:
                    data[key] = self.absolute_degree_of_disorder()
        else:
            matches = find_matching_interval_keys(
                self.template_file_path, self.verification_file_path
            )
            for key in matches:
                if self.absolute_degree_of_disorder(True) < self.THRESHOLD:
                    data[key] = self.absolute_degree_of_disorder(True)
        return data
