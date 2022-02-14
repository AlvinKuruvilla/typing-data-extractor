# Copyright 2020-2021, Alvin Kuruvilla <alvineasokuruvilla@gmail.com>

# Use of this source code is governed by an MIT-style
# license that can be found in the LICENSE file or at
# https://opensource.org/licenses/MIT.

from core.td_data_dict import TD_Data_Dictionary
from .verifier_utils import find_matching_keys, is_between, find_matching_interval_keys
from core.log import Logger


class AbsoluteVerifier:
    def __init__(
        self, template_file_path: str, verification_file_path: str, threshold: float
    ):
        self.THRESHOLD = threshold
        self.template_file_path = template_file_path
        self.verification_file_path = verification_file_path
        self.template_td_data_dict = TD_Data_Dictionary(self.template_file_path)
        self.verification_td_data_dict = TD_Data_Dictionary(self.verification_file_path)

    def class_name() -> str:
        return "Absolute Verifier"

    def template_path(self):
        return self.template_file_path

    def verification_path(self):
        return self.verification_file_path

    def is_key_valid(self, key: str, use_kit=False) -> bool:
        if use_kit == False:
            latencies = self.find_latency_averages(key)
            assert len(latencies) == 2
            return self.check_key_hold_latencies(key)
        else:
            latencies = self.find_latency_averages(key, True)
            assert len(latencies) == 2
            return self.check_key_interval_latencies(key)

    def calculate_absolute_score(self, use_kit=False):
        if use_kit == False:
            matches = find_matching_keys(
                self.template_file_path, self.verification_file_path
            )
            valids = self.find_all_valid_keys()
            return 1 - (len(valids) / len(matches))
        else:
            matches = find_matching_interval_keys(
                self.template_file_path, self.verification_file_path
            )
            valids = self.find_all_valid_keys(True)
            return 1 - (len(valids) / len(matches))

    def find_latency_averages(self, key: str, use_kit=False):
        log = Logger("find_latency_averages")
        if use_kit == False:
            # NOTE: This function does not actually calculate the average latency
            # for the key, rather it perform a lookup on the dictionary returned by calculate_key_hit_time()
            # function for both of the td_data_dict's.
            # This is because the returned KHT dictionary already performs a mean operation if there are
            # multiple latencies for a particular key
            template_hit_dict = self.template_td_data_dict.calculate_key_hold_time()
            verification_hit_dict = (
                self.verification_td_data_dict.calculate_key_hold_time()
            )
            key_matches = find_matching_keys(
                self.template_file_path, self.verification_file_path
            )
            if not key in key_matches:
                log.km_error("Key not found")
                return
            t_latency = template_hit_dict.get(key)
            v_latency = verification_hit_dict.get(key)
            return [t_latency, v_latency]
        else:
            template_pairs = self.template_td_data_dict.get_key_pairs()
            verification_pairs = self.verification_td_data_dict.get_key_pairs()
            template_inteval_dict = (
                self.template_td_data_dict.calculate_key_interval_time(template_pairs)
            )
            verification_inteval_dict = (
                self.verification_td_data_dict.calculate_key_interval_time(
                    verification_pairs
                )
            )
            key_matches = find_matching_interval_keys(
                self.template_file_path, self.verification_file_path
            )
            if not key in key_matches:
                log.km_error("Key not found")
                return
            t_latency = template_inteval_dict.get(key)
            v_latency = verification_inteval_dict.get(key)
            return [t_latency, v_latency]

    def find_all_valid_keys(self, use_kit=False):
        valids = []
        if use_kit == False:
            matches = find_matching_keys(
                self.template_file_path, self.verification_file_path
            )
            for key in matches:
                if self.is_key_valid(key):
                    valids.append(key)
            return valids
        else:
            matches = find_matching_interval_keys(
                self.template_file_path, self.verification_file_path
            )
            for key in matches:
                if self.is_key_valid(key, True):
                    valids.append(key)
            return valids

    def check_key_hold_latencies(self, key: str):
        latencies = self.find_latency_averages(key)
        assert len(latencies) == 2
        if latencies[0] > latencies[1]:
            avg = latencies[0] / latencies[1]
            if is_between(avg, 1.0, self.THRESHOLD):
                return True
            else:
                return False
        elif latencies[0] < latencies[1]:
            avg = latencies[1] / latencies[0]
            if is_between(avg, 1.0, self.THRESHOLD):
                return True
            else:
                return False
        elif latencies[0] == latencies[1]:
            # If the two latnecies are equal than we know the quotient between them will always be 1
            # and thus, always fall in the inclusive range of (1, THRESHOLD) so we can automatically
            # just return True
            return True

    def check_key_interval_latencies(self, key: str):
        latencies = self.find_latency_averages(key, True)
        assert len(latencies) == 2
        i = 0
        for i in range(len(latencies[0])):
            if latencies[0][i] > latencies[1][i]:
                avg = latencies[0][i] / latencies[1][i]
                if is_between(avg, 1.0, self.THRESHOLD):
                    return True
                else:
                    return False
            elif latencies[0][i] < latencies[1][i]:
                avg = latencies[0][i] / latencies[1][i]
                if is_between(avg, 1.0, self.THRESHOLD):
                    return True
                else:
                    return False
            elif latencies[0][i] == latencies[1][i]:
                # If the two latnecies are equal than we know the quotient between them will always be 1
                # and thus, always fall in the inclusive range of (1, THRESHOLD) so we can automatically
                # just return True
                return True

    def get_threshold(self):
        return self.threshold

    def set_threshold(self, threshold):
        self.threshold = threshold

    def count_valid_key_matches(self):
        return len(self.find_all_valid_keys())

    def count_valid_interval_key_matches(self):
        return len(self.find_all_valid_keys(True))
