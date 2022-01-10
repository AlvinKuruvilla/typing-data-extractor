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
        metavar="path",
        type=str,
        help="The path to the csv file to extract typing dynamics data from",
    )
    args = args_parser.parse_args(argv)
    input_path = args.Path

    if not is_csv_file(input_path):
        sys.exit()
    data_dict = TD_Data_Dictionary(input_path)
    # data_dict.calculate_key_hit_time()
    # data_dict.debug()
    pairs = data_dict.get_key_pairs()

    #print(pairs)
    data_dict.calculate_key_interval_time(pairs)
if __name__ == "__main__":
    exit(main())
