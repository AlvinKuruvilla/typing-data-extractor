# Copyright 2020-2021, Alvin Kuruvilla <alvineasokuruvilla@gmail.com>

# Use of this source code is governed by an MIT-style
# license that can be found in the LICENSE file or at
# https://opensource.org/licenses/MIT.

from converters.pickle_driver import PickleDriver
from core.td_data_dict import TD_Data_Dictionary
from core.td_utils import (
    find_matching_keys,
    is_between,
    find_matching_interval_keys,
    read_matching_keys_from_files,
)
from core.log import Logger
from rich.traceback import install
from core.utils import running_avg

install()


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

    def set_template_file_path(self, new_path: str) -> None:
        self.template_file_path = new_path

    def set_verification_file_path(self, new_path: str) -> None:
        self.verification_file_path = new_path

    def template_path(self):
        return self.template_file_path

    def verification_path(self):
        return self.verification_file_path

    def is_key_valid(self, key: str, use_kit=False, is_evaluating=False) -> bool:
        if is_evaluating == False:
            if use_kit == False:
                return self.check_key_hold_latencies(key)
            else:
                return self.check_key_interval_latencies(key)
        if is_evaluating == True:
            if use_kit == False:
                return self.check_key_hold_latencies(key, is_evaluating=True)
            else:
                return self.check_key_interval_latencies(key, is_evaluating=True)

    def calculate_absolute_score(self, use_kit=False, is_evaluating=False):
        if is_evaluating == False:
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
                valids = self.find_all_valid_keys(use_kit=True)
                return 1 - (len(valids) / len(matches))
        elif is_evaluating == True:
            if use_kit == False:
                matches = read_matching_keys_from_files(
                    self.template_file_path, self.verification_file_path
                )
                valids = self.find_all_valid_keys(is_evaluating=True)
                return 1 - (len(valids) / len(matches))
            else:
                matches = read_matching_keys_from_files(
                    self.template_file_path, self.verification_file_path
                )
                valids = self.find_all_valid_keys(use_kit=True, is_evaluating=True)
                return 1 - (len(valids) / len(matches))

    def find_latency_averages(self, key: str, use_kit=False, is_evaluating=False):
        log = Logger("find_latency_averages")
        if is_evaluating == False:
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
                    self.template_td_data_dict.calculate_key_interval_time(
                        template_pairs
                    )
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
        elif is_evaluating == True:
            # Read the KHT and KIT values from the files
            key_matches = read_matching_keys_from_files(
                self.template_file_path, self.verification_file_path
            )
            if not key in key_matches:
                log.km_error("Key not found")
                return
            driver = PickleDriver()
            # NOTE: THESE PATHS MUST POINT TO FILES CONTAINING KIT DATA
            template_inteval_dict = driver.load_as_dictionary(self.template_file_path)
            verification_inteval_dict = driver.load_as_dictionary(
                self.verification_file_path
            )
            t_latency = template_inteval_dict.get(key)
            v_latency = verification_inteval_dict.get(key)
            return [t_latency, v_latency]

    def find_all_valid_keys(self, use_kit=False, is_evaluating=False):
        valids = []
        if is_evaluating == False:
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
                print("Found", matches)
                for key in matches:
                    if self.is_key_valid(key, use_kit=True):
                        valids.append(key)
                return valids
        elif is_evaluating == True:
            matches = read_matching_keys_from_files(
                self.template_file_path, self.verification_file_path
            )
            if use_kit == False:
                for key in matches:
                    if self.is_key_valid(key, is_evaluating=True):
                        valids.append(key)
                return valids
            elif use_kit == True:
                for key in matches:
                    if self.is_key_valid(key, is_evaluating=True, use_kit=True):
                        valids.append(key)
                return valids

    def check_key_hold_latencies(self, key: str, is_evaluating=False):
        if is_evaluating == False:
            latencies = self.find_latency_averages(key)
            assert len(latencies) == 2
            if latencies[0] > latencies[1]:
                avg = running_avg(latencies[0]) / running_avg(latencies[1])
                if is_between(avg, 1.0, self.THRESHOLD):
                    return True
                else:
                    return False
            elif latencies[0] < latencies[1]:
                avg = running_avg(latencies[1]) / running_avg(latencies[0])
                if is_between(avg, 1.0, self.THRESHOLD):
                    return True
                else:
                    return False
            elif latencies[0] == latencies[1]:
                # If the two latnecies are equal than we know the quotient between them will always be 1
                # and thus, always fall in the inclusive range of (1, THRESHOLD) so we can automatically
                # just return True
                return True
        elif is_evaluating == True:
            latencies = self.find_latency_averages(key, is_evaluating=True)
            assert len(latencies) == 2
            if latencies[0] > latencies[1]:
                avg = running_avg(latencies[0]) / running_avg(latencies[1])
                if is_between(avg, 1.0, self.THRESHOLD):
                    return True
                else:
                    return False
            elif latencies[0] < latencies[1]:
                avg = running_avg(latencies[1]) / running_avg(latencies[0])
                if is_between(avg, 1.0, self.THRESHOLD):
                    return True
                else:
                    return False
            elif latencies[0] == latencies[1]:
                # If the two latnecies are equal than we know the quotient between them will always be 1
                # and thus, always fall in the inclusive range of (1, THRESHOLD) so we can automatically
                # just return True
                return True

    def check_key_interval_latencies(self, key: str, is_evaluating=False):
        if is_evaluating == False:
            latencies = self.find_latency_averages(key, use_kit=True)
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
        elif is_evaluating == True:
            latencies = self.find_latency_averages(
                key, use_kit=True, is_evaluating=True
            )
            assert len(latencies) == 2
            i = 0
            for i in range(len(latencies[0])):
                if latencies[0][i] > latencies[1][i]:
                    avg = running_avg(latencies[0][i]) / running_avg(latencies[1][i])
                    # print("Average", avg)
                    # input("Hang")
                    if is_between(running_avg(avg), 1.0, self.THRESHOLD):
                        return True
                    else:
                        return False
                elif latencies[0][i] < latencies[1][i]:
                    avg = running_avg(latencies[1][i]) / running_avg(latencies[0][i])
                    if is_between(running_avg(avg), 1.0, self.THRESHOLD):
                        return True
                    else:
                        return False
                elif latencies[0][i] == latencies[1][i]:
                    # If the two latnecies are equal than we know the quotient between them will always be 1
                    # and thus, always fall in the inclusive range of (1, THRESHOLD) so we can automatically
                    # just return True
                    return True
            pass

    def get_threshold(self):
        return self.threshold

    def set_threshold(self, threshold):
        self.threshold = threshold

    def count_valid_key_matches(self, is_evaluating=False):
        if is_evaluating == False:
            return len(self.find_all_valid_keys())
        elif is_evaluating == True:
            return len(self.find_all_valid_keys(is_evaluating=True))

    def count_valid_interval_key_matches(self, is_evaluating=False):
        if is_evaluating == False:
            return len(self.find_all_valid_keys(use_kit=True))
        elif is_evaluating == True:
            return len(self.find_all_valid_keys(use_kit=True, is_evaluating=True))
