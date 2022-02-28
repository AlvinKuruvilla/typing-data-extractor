# Copyright 2022, Alvin Kuruvilla <alvineasokuruvilla@gmail.com>

# Use of this source code is governed by an MIT-style
# license that can be found in the LICENSE file or at
# https://opensource.org/licenses/MIT.

#! FIXME: When running the CLI using two bbmass generated data files execution takes exceedingly long (11+ minutes at minimum)
import argparse
import sys
from typing import Optional, Sequence
from core.td_data_dict import TD_Data_Dictionary

from core.utils import is_csv_file
from extractors.word_level_extractor import WordExtractor
from verifiers.absolute_verifier import AbsoluteVerifier

from rich.traceback import install

# from verifiers.evaluator import Verifier_Evaluator, validate_verifier_type
import os

# import matplotlib.pyplot as plt

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
    verifier = AbsoluteVerifier(input_path, other_path, 2.0)
    verifier.set_template_file_path("KHT_gen_User1.txt")
    verifier.set_verification_file_path("KHT_gen_User3.txt")
    # print(verifier.find_all_valid_keys(is_evaluating=True))
    # f1 = os.path.join(os.getcwd(), "testdata", "g1.csv")
    # f2 = os.path.join(os.getcwd(), "testdata", "g3.csv")
    # d = TD_Data_Dictionary(f1)
    # d2 = TD_Data_Dictionary(f2)
    # driver = PickleDriver()
    # k = d.make_kht_dictionary()
    # k2 = d2.make_kht_dictionary()
    # driver.write_kht_dictionary_to_file(k, "gen_User1.txt")
    # driver.write_kht_dictionary_to_file(k2, "gen_User3.txt")
    d1 = TD_Data_Dictionary(os.path.join(os.getcwd(), "testdata", "456.csv"))
    d2 = TD_Data_Dictionary(os.path.join(os.getcwd(), "testdata", "789.csv"))
    we = WordExtractor(d1, d2)
    words = we.get_words(d1)
    print(words)


if __name__ == "__main__":
    exit(main())
