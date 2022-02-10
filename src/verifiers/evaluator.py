# Copyright 2020-2021, Alvin Kuruvilla <alvineasokuruvilla@gmail.com>

# Use of this source code is governed by an MIT-style
# license that can be found in the LICENSE file or at
# https://opensource.org/licenses/MIT.

from bbmass_conv import NotCSVFileError
from utils import is_csv_file
from verifiers.relative_verifier import RelativeVerifier
from verifiers.absolute_verifier import AbsoluteVerifier
from verifiers.similarity_verifier import SimilarityVerifier
from verifiers.verifier_utils import *
import os


class Invalid_Verifier(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


def evaluate_against_file(template_path, other_filepath, verifier, use_interval=False):
    if not is_csv_file(template_path):
        raise NotCSVFileError(template_path, template_path + " is not a CSV file")
    if not is_csv_file(other_filepath):
        raise NotCSVFileError(other_filepath, other_filepath + " is not a CSV file")
    if not validate_verifier_type(verifier):
        raise Invalid_Verifier("Provided verifier is not a valid type")
    if use_interval == False:
        total_matches = count_key_matches(template_path, other_filepath)
        valid_matches = verifier.count_valid_key_matches()
        percent = valid_matches / total_matches
        return (percent, is_majority(percent))
    elif use_interval == True:
        total_matches = count_interval_key_matches(template_path, other_filepath)
        valid_matches = verifier.count_valid_interval_key_matches()
        percent = valid_matches / total_matches
        return (percent, is_majority(percent))


def evaluate_against_directory(
    template_path: str, directory_path: str, verifier, use_interval=False
):
    if not is_csv_file(template_path):
        raise NotCSVFileError(template_path, template_path + " is not a CSV file")
    if not os.path.isdir(directory_path):
        raise ValueError(directory_path + " is not a directory")
    for file in os.listdir(directory_path):
        if not is_csv_file(file):
            raise NotCSVFileError(file, file + " is not a CSV file")
        if use_interval == False:
            total_matches = count_key_matches(template_path, file)
            valid_matches = verifier.count_valid_key_matches()
            percent = valid_matches / total_matches
            print(file, percent, is_majority(percent))
        elif use_interval == True:
            total_matches = count_interval_key_matches(template_path, file)
            valid_matches = verifier.count_valid_interval_key_matches()
            percent = valid_matches / total_matches
            print(file, percent, is_majority(percent))


def is_majority(percent: float):
    if percent > 0.50:
        return True
    else:
        return False


def validate_verifier_type(verifier):
    if isinstance(verifier, RelativeVerifier):
        return True
    elif isinstance(verifier, AbsoluteVerifier):
        return True
    elif isinstance(verifier, SimilarityVerifier):
        return True
    else:
        return False


class Verifier_Evaluator:
    def __init__(self, verifier, threshold):
        if validate_verifier_type(verifier):
            self.verifier = verifier
            self.threshold = threshold
        else:
            raise Invalid_Verifier("Provided verifier is not a valid type")

    def extract_features(self):
        kht_valids = self.verifier.find_all_valid_keys()
        kit_valids = self.verifier.find_all_valid_keys(True)
        return (kht_valids, kit_valids)

    def evaluate(self, kht_valids, kit_valids):
        t_path = self.get_template_file_path()
        v_path = self.get_verification_file_path()
        total_kht = find_matching_keys(t_path, v_path)
        total_kit = find_matching_interval_keys(t_path, v_path)
        # Now that we have the number of actual matches and the number of total potential matches
        # we can just divide them and see if they exceed a threshold
        kht_percent = len(kht_valids) / len(total_kht)
        kit_percent = len(kit_valids) / len(total_kit)
        if kht_percent > self.threshold and kit_percent > self.threshold:
            return tuple("True")
        else:
            return tuple("False")

    def get_template_file_path(self):
        return self.verifier.template_path()

    def get_verification_file_path(self):
        return self.verifier.verification_path()

    def switch_verifier(self, new_verifier):
        if validate_verifier_type(new_verifier):
            self.verifier = new_verifier
        else:
            raise Invalid_Verifier("Provided verifier is not a valid type")

    def get_threshold(self):
        return self.threshold

    def set_threshold(self, threshold):
        self.threshold = threshold
