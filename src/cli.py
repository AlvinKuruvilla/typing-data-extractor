import argparse
import sys
from typing import Optional, Sequence

from utils import is_csv_file, pretty_print
from ops import TDOps


def main(argv: Optional[Sequence[str]] = None) -> int:

    args_parser = argparse.ArgumentParser(
        description='Extract typing dynamics data from a csv file')
    args_parser.add_argument(
        "Path",
        metavar="path",
        type=str,
        help='The path to the file to extract typing dynamics data from',
    )
    args = args_parser.parse_args(argv)
    input_path = args.Path

    if not is_csv_file(input_path):
        sys.exit()
    td = TDOps()
    (td.calculate_key_hit_time(input_path))
    # td.calculate_key_interval_time(input_path)


if __name__ == '__main__':
    exit(main())
