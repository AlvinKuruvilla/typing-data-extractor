# Copyright 2022, Alvin Kuruvilla <alvineasokuruvilla@gmail.com>

# Use of this source code is governed by an MIT-style
# license that can be found in the LICENSE file or at
# https://opensource.org/licenses/MIT.

import argparse
from pprint import pprint
import sys
from typing import Optional, Sequence
from converters.pickle_driver import PickleDriver
from core.td_data_dict import TD_Data_Dictionary, KIT_Type
from rich.traceback import install
from core.utils import is_csv_file
from verifiers.absolute_verifier import AbsoluteVerifier
from verifiers.evaluator import evaluate_against_files
import os

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
    # data_dict = TD_Data_Dictionary(input_path)
    driver = PickleDriver()
    # print(pairs)

    # data_dict = TD_Data_Dictionary(input_path)
    # comp_dict = TD_Data_Dictionary(other_path)
    # kht = data_dict.make_kht_dictionary()
    # kht2 = comp_dict.make_kht_dictionary()
    # kit = data_dict.make_kit_dictionary(pairs, KIT_Type.Press_Press)

    f = os.path.join(os.getcwd(), "testdata", "456.csv")
    f2 = os.path.join(os.getcwd(), "testdata", "789.csv")
    verifier = AbsoluteVerifier(f, f2, 2.0)

    valids = verifier.find_all_valid_keys(use_kit=True)
    # print("Valids:", valids)
    # TODO: To test KIT and eval we have to first generate pickled kit files for "testdata/456.csv" and "testdata/789.csv"
    # and then change the verifiers paths to point to them
    verifier.set_template_file_path("KHT_test.txt")
    verifier.set_verification_file_path("KHT_test3.txt")
    other_valids = verifier.find_all_valid_keys(is_evaluating=True)
    # print("Other valids:", other_valids)

    data_dict = TD_Data_Dictionary(f)
    comp_dict = TD_Data_Dictionary(f2)
    pairs = data_dict.get_key_pairs()
    cpairs = comp_dict.get_key_pairs()
    # kht = data_dict.make_kht_dictionary()
    # kht2 = comp_dict.make_kht_dictionary()
    # driver.write_kht_dictionary_to_file(kht, "test.txt")
    # driver.write_kht_dictionary_to_file(kht2, "test3.txt")
    # pprint(driver.load_as_dictionary("KHT_test3.txt"))
    kit = data_dict.make_kit_dictionary(pairs, KIT_Type.Press_Press)
    kit2 = comp_dict.make_kit_dictionary(cpairs, KIT_Type.Press_Press)
    # pprint(kht)
    # driver.write_kht_dictionary_to_file(kht, gen_file)
    driver.write_kit_dictionary_to_file(kit, KIT_Type.Press_Press, "KIT1.txt")
    driver.write_kit_dictionary_to_file(kit2, KIT_Type.Press_Press, "KIT2.txt")
    # TODO: Why is there such a big difference between the two verifier passes with and without the eval???
    verifier.set_template_file_path("KIT_PP_KIT1.txt")
    verifier.set_verification_file_path("KIT_PP_KIT2.txt")
    # print("From file:", driver.read_to_list("KIT_PP_KIT1.txt"))
    ################################################################
    other_valids = verifier.find_all_valid_keys(is_evaluating=True, use_kit=True)
    print("With evaluation", other_valids)
    print(len(other_valids))
    input()
    ################################################################

    other_verifier = AbsoluteVerifier(input_path, other_path, 2.0)
    other_other_valids = other_verifier.find_all_valid_keys(
        is_evaluating=False, use_kit=True
    )
    print("Without evaluation", len(other_other_valids))


# print(len(other_other_valids) == len(other_valids))

# print(driver.load_as_dictionary("KHT_pickled_User1.txt"))
# print(data_dict.make_kht_dictionary())
# print(evaluate_against_files(f, f2, verifier))


if __name__ == "__main__":
    exit(main())
