# Copyright 2022, Alvin Kuruvilla <alvineasokuruvilla@gmail.com>

# Use of this source code is governed by an MIT-style
# license that can be found in the LICENSE file or at
# https://opensource.org/licenses/MIT.

import statistics
from core.log import Logger
from core.td_utils import find_matching_keys, find_matching_interval_keys
from core.td_data_dict import TD_Data_Dictionary
from rich.traceback import install

install()


class SimilarityVerifier:
    def __init__(self, template_file_path: str, verification_file_path: str, threshold):
        self.template_file_path = template_file_path
        self.verification_file_path = verification_file_path
        self.template_td_data_dict = TD_Data_Dictionary(self.template_file_path)
        self.verification_td_data_dict = TD_Data_Dictionary(self.verification_file_path)
        self.THRESHOLD = threshold

    __slots__ = (
        "template_file_path",
        "verification_file_path",
        "THRESHOLD",
        "template_td_data_dict",
        "verification_td_data_dict",
    )

    def class_name(self) -> str:
        return "Similarity Verifier"

    def template_path(self):
        return self.template_file_path

    def set_threshold(self, threshold):
        self.threshold = threshold

    def get_threshold(self):
        return self.THRESHOLD

    def verification_path(self):
        return self.verification_file_path

    def set_template_file_path(self, new_template_file_path: str):
        self.template_file_path = new_template_file_path

    def set_verification_file_path(self, new_verification_file_path: str):
        self.verification_file_path = new_verification_file_path

    def calculate_standard_deviation(self, data: list):
        sdev = statistics.pstdev(data)
        return sdev

    def find_latency_averages(self, key: str, use_kit=False):
        log = Logger("similarity_find_latency_averages")
        # NOTE: This function does not actually calculate the average latency
        # for the key, rather it perform a lookup on the dictionary returned by calculate_key_hold_time()
        # function for both of the td_data_dict's.
        # This is because the returned KHT dictionary already performs a mean operation if there are
        # multiple latencies for a particular key
        if use_kit == False:
            template_hit_dict = self.template_td_data_dict.calculate_key_hold_time()
            verification_hit_dict = (
                self.verification_td_data_dict.calculate_key_hold_time()
            )
            key_matches = find_matching_keys(
                self.template_file_path, self.verification_file_path
            )
            if not key in key_matches:
                log.km_error("Key %s not found" % key)
                return
            t_latency = template_hit_dict.get(key)
            v_latency = verification_hit_dict.get(key)
            return [t_latency, v_latency]
        elif use_kit == True:
            template_pairs = self.template_td_data_dict.get_key_pairs()
            verification_pairs = self.verification_td_data_dict.get_key_pairs()
            template_hit_dict = self.template_td_data_dict.calculate_key_interval_time(
                template_pairs
            )
            verification_hit_dict = (
                self.verification_td_data_dict.calculate_key_interval_time(
                    verification_pairs
                )
            )
            key_matches = find_matching_interval_keys(
                self.template_file_path, self.verification_file_path
            )
            if not key in key_matches:
                log.km_error("Key %s not found" % key)
                return
            # TODO: Double check that this is what we actually want to do here
            t_latency = template_hit_dict.get(key)
            v_latency = verification_hit_dict.get(key)
            return [t_latency, v_latency]

    def calculate_similarity_score(self, use_kit=False):
        if use_kit == False:
            matches = find_matching_keys(
                self.template_file_path, self.verification_file_path
            )
            valids = self.find_all_valid_keys()
            return 1 - (len(valids) / len(matches))
        elif use_kit == True:
            matches = find_matching_interval_keys(
                self.template_file_path, self.verification_file_path
            )
            valids = self.find_all_valid_keys(use_kit=True)
            return 1 - (len(valids) / len(matches))

    def is_key_valid(self, key: str, use_kit=False) -> bool:
        if use_kit == False:
            latencies = self.find_latency_averages(key)
            assert len(latencies) == 2
            sdev = self.calculate_standard_deviation(latencies)
            # print("The standard deviation is: ", sdev)
            if sdev <= self.THRESHOLD:
                return True
            else:
                return False
        elif use_kit == True:
            latencies = self.find_latency_averages(key, use_kit=True)
            assert len(latencies) == 2
            sdev = self.calculate_standard_deviation(latencies)
            # print("The standard deviation is: ", sdev)
            if sdev <= self.THRESHOLD:
                return True
            else:
                return False

    def find_all_valid_keys(self, use_kit=False):
        if use_kit == False:
            valids = []
            matches = find_matching_keys(
                self.template_file_path, self.verification_file_path
            )
            for key in matches:
                if self.is_key_valid(key):
                    valids.append(key)
            print("Valids: ", valids)
            return valids
        elif use_kit == True:
            valids = []
            matches = find_matching_interval_keys(
                self.template_file_path, self.verification_file_path
            )
            for key in matches:
                if self.is_key_valid(key):
                    valids.append(key)
            print("Valids: ", valids)
            return valids

    def count_valid_key_matches(self, use_kit=False):
        if use_kit == False:
            return len(self.find_all_valid_keys())
        elif use_kit == True:
            return len(self.find_all_valid_keys(use_kit=True))
