import argparse
import sys
from typing import Optional, Sequence
from td_data_dict import TD_Data_Dictionary

from utils import is_csv_file


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
    # data_dict.calculate_key_hit_time()
    # data_dict.debug()
    # pairs = data_dict.get_key_pairs()

    #print(pairs)
    # data_dict.calculate_key_interval_time(pairs)
if __name__ == "__main__":
    exit(main())
