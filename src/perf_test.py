# Copyright 2022, Alvin Kuruvilla <alvineasokuruvilla@gmail.com>

# Use of this source code is governed by an MIT-style
# license that can be found in the LICENSE file or at
# https://opensource.org/licenses/MIT.

import argparse
import sys
from typing import Optional, Sequence
from pickle_driver import PickleDriver
from td_data_dict import TD_Data_Dictionary, KIT_Type
from rich.traceback import install
from utils import is_csv_file
from verifiers.absolute_verifier import AbsoluteVerifier
from verifiers.evaluator import evaluate_against_dictionaries
from pprint import pprint

install()


def main(argv: Optional[Sequence[str]] = None) -> int:
    args_parser = argparse.ArgumentParser(
        description="Extract typing dynamics data from a csv file"
    )
    args_parser.add_argument(
        "Path",
        metavar="First Path",
        type=str,
        help="The path to the first csv file to extract typing dynamics data from",
    )
    args_parser.add_argument(
        "Other",
        metavar="Other Path",
        type=str,
        help="The path to the other csv file to extract typing dynamics data from",
    )
    args = args_parser.parse_args(argv)
    input_path = args.Path
    other_path = args.Other

    if not is_csv_file(input_path) or not is_csv_file(other_path):
        sys.exit()
    data_dict = TD_Data_Dictionary(input_path)
    driver = PickleDriver()
    pairs = data_dict.get_key_pairs()
    # print(pairs)
    r_verifier = AbsoluteVerifier(input_path, other_path, 1.0)
    # r_verifier.find_all_valid_keys()
    data_dict = TD_Data_Dictionary(input_path)
    comp_dict = TD_Data_Dictionary(other_path)
    kht = data_dict.make_kht_dictionary()
    kht2 = comp_dict.make_kht_dictionary()
    kit = data_dict.make_kit_dictionary(pairs, KIT_Type.Press_Press)
    driver.wipe_file("test.txt")
    driver.write_kht_dictionary_to_file(kht, "test.txt")
    driver.write_kit_dictionary_to_file(kit, KIT_Type.Press_Press, "test.txt")
    # pprint(driver.read_to_list("KHT_test.txt"))
    verifier = AbsoluteVerifier(input_path, other_path, 2.0)
    evaluate_against_dictionaries(kht, kht2, verifier)
    # print(data_dict.make_kht_dictionary())
    # print(KIT_Type.Press_Press is KIT_Type.Press_Release)


if __name__ == "__main__":
    exit(main())
