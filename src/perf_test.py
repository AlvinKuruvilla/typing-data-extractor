import argparse
import sys
from typing import Optional, Sequence
from td_data_dict import TD_Data_Dictionary, KIT_Type
from rich.traceback import install
from utils import is_csv_file
from verifiers.absolute_verifier import AbsoluteVerifier
from verifiers.evaluator import evaluate_against_file

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
    # pairs = data_dict.get_key_pairs()
    # print(pairs)
    r_verifier = AbsoluteVerifier(input_path, other_path, 1.0)
    # r_verifier.find_all_valid_keys()
    data_dict = TD_Data_Dictionary(input_path)
    verifier = AbsoluteVerifier(input_path, other_path, 2.0)
    print(evaluate_against_file(input_path, other_path, verifier))
    print(data_dict.make_kht_dictionary())
    print(KIT_Type.Press_Press is KIT_Type.Press_Release)


if __name__ == "__main__":
    exit(main())
