# NOTE: Uses the KIHT value

from math import pow
from td_data_dict import TD_Data_Dictionary
from log import Logger
from typing import List, Optional

# NOTE: As far as I can tell this verifier operates on the entire set of verification data
# i.e. it considers all the KHT values from the verification data as a whole sample and then compares the whole thing
# to the entire set of template data which is treated similarly
# For our use case we may want to treat each KHT value as its own individual sample and
# then only compare it to the corresponding KHT in the template data.


class RelativeVerifier:
    def __init__(
        self, template_file_path: str, verification_file_path: str, threshold: float
    ) -> None:
        self.THRESHOLD = threshold
        self.template_file_path = template_file_path
        self.verification_file_path = verification_file_path
        self.template_td_data_dict = TD_Data_Dictionary(self.template_file_path)
        self.verification_td_data_dict = TD_Data_Dictionary(self.verification_file_path)
        self.template_table = self.get_table(self.template_file_path, True)
        self.verification_table = self.get_table(self.verification_file_path)

    def get_table(self, path: str, sort_keys: bool = False) -> Optional[List[int]]:
        log = Logger()
        if path == self.template_file_path:
            if sort_keys:
                return list(self.template_td_data_dict.values()).sort()
            else:
                return list(self.template_td_data_dict.values())
        elif path == self.verification_file_path:
            if sort_keys:
                return list(self.verification_td_data_dict.values()).sort()
            else:
                return list(self.verification_td_data_dict.values())
        else:
            log.km_fatal(
                "The provided path"
                + path
                + "does not match the template or verification file paths"
            )
            return None

    def degree_of_disorder(self) -> int:
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
        for entry in self.verification_table:
            disorder += self.find_distance(entry)
        return disorder

    def absolute_degree_of_disorder(self) -> float:
        # The formula to calculate the absolute degree of disorder is simply:
        #   1) Find the degree of disorder for the entire table
        #   2) Calculate the maximum degree of disorder for a table with n elements accroding to the formula (n^2 -1)/2
        #   3) Divide the degree of disorder with the maximum calculated in the previous step
        return self.degree_of_disorder() / self.absolute_degree_of_disorder()

    def max_degree_of_disorder(self) -> float:
        # To calculate the maximum degree of disorder for a table with n elements use the formula (n^2 -1)/2
        n = len(self.verification_table)
        return (pow(n, 2) - 1) / 2

    def is_valid(self) -> bool:
        # Maybe to see if typing samples are valid we compare the absolute degree of disorder with a given
        # threshold value and if it is less than the threshold the sample is considered valid
        if self.absolute_degree_of_disorder() < self.THRESHOLD:
            return True
        else:
            return False

    def find_distance(self, entry) -> int:
        # Finds the distance between a given entry from the template table and
        # the corresponding entry in the verification table
        log = Logger()
        distance = 0
        if not entry in self.template_table:
            log.km_fatal(
                "Provided entry" + entry + "is not in the sorted template table"
            )
            return
        if not entry in self.verification_table:
            log.km_fatal("Provided entry" + entry + "is not in the verification table")
            return
        for cell in self.verification_table:
            if cell == entry:
                return distance
            else:
                distance += 1
        return distance

    def template_path(self):
        return self.template_file_path

    def verification_path(self):
        return self.verification_file_path
