import argparse
import sys
from typing import Optional, Sequence
from td_data_dict import TD_Data_Dictionary
from verifiers.absolute_verifier import AbsoluteVerifier
from utils import is_csv_file
from verifiers.relative_verifier import RelativeVerifier
from rich.traceback import install
from verifiers.verifier_utils import find_matching_interval_keys

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
    # data_dict.calculate_key_interval_time(pairs)

    comp_dict = TD_Data_Dictionary(other_path)
    # comp_dict.key_hit_time_keys()
    # hits = data_dict.calculate_key_hit_time()
    comp_dict.calculate_key_hold_time()
    # print(find_matching_keys(input_path, other_path))
    r_verifier = RelativeVerifier(input_path, other_path, 2.0)
    # r_verifier.find_all_valid_keys(True)
    matches = find_matching_interval_keys(input_path, other_path)
    print(r_verifier.find_all_valid_keys())


if __name__ == "__main__":
    exit(main())
