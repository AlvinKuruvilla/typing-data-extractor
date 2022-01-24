# NOTE: Uses the KIHT value

import statistics
from log import Logger
from .verifier_utils import find_matching_keys
from td_data_dict import TD_Data_Dictionary


class SimilarityVerifier:
    def __init__(
        self,
        template_file_path: str,
        verification_file_path: str,
    ):
        self.template_file_path = template_file_path
        self.verification_file_path = verification_file_path
        self.template_td_data_dict = TD_Data_Dictionary(self.template_file_path)
        self.verification_td_data_dict = TD_Data_Dictionary(self.verification_file_path)

    def template_path(self):
        return self.template_file_path

    def set_threshold(self, threshold):
        self.threshold = threshold

    def get_threshold(self):
        return self.threshold

    def verification_path(self):
        return self.verification_file_path

    def calculate_standard_deviation(self, data: list):
        sdev = statistics.pstdev(data)
        return sdev

    def find_latency_averages(self, key: str):
        log = Logger()
        # NOTE: This function does not actually calculate the average latency
        # for the key, rather it perform a lookup on the dictionary returned by calculate_key_hit_time()
        # function for both of the td_data_dict's.
        # This is because the returned KHT dictionary already performs a mean operation if there are
        # multiple latencies for a particular key
        template_hit_dict = self.template_td_data_dict.calculate_key_hit_time()
        verification_hit_dict = self.verification_td_data_dict.calculate_key_hit_time()
        key_matches = find_matching_keys(
            self.template_file_path, self.verification_file_path
        )
        if not key in key_matches:
            log.km_error("Key %s not found" % key)
            return
        t_latency = template_hit_dict.get(key)
        v_latency = verification_hit_dict.get(key)
        return [t_latency, v_latency]

    def calculate_similarity_score(self):
        matches = find_matching_keys(
            self.template_file_path, self.verification_file_path
        )
        valids = self.find_all_valid_keys()
        return 1 - (len(valids) / len(matches))

    def is_key_valid(self, key: str) -> bool:
        latencies = self.find_latency_averages(key)
        assert len(latencies) == 2
        sdev = self.calculate_standard_deviation(latencies)
        # print("The standard deviation is: ", sdev)
        if sdev <= 1:
            return True
        else:
            return False

    def find_all_valid_keys(self):
        valids = []
        matches = find_matching_keys(
            self.template_file_path, self.verification_file_path
        )
        for key in matches:
            if self.is_key_valid(key):
                valids.append(key)
        print("Valids: ", valids)
