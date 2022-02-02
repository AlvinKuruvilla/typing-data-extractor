# Copyright 2020-2021, Alvin Kuruvilla <alvineasokuruvilla@gmail.com>

# Use of this source code is governed by an MIT-style
# license that can be found in the LICENSE file or at
# https://opensource.org/licenses/MIT.

from verifiers.relative_verifier import RelativeVerifier
from verifiers.absolute_verifier import AbsoluteVerifier
from verifiers.similarity_verifier import SimilarityVerifier
from verifiers.verifier_utils import find_matching_keys, find_matching_interval_keys


class Invalid_Verifier(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


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
