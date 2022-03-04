# Copyright 2022, Alvin Kuruvilla <alvineasokuruvilla@gmail.com>

# Use of this source code is governed by an MIT-style
# license that can be found in the LICENSE file or at
# https://opensource.org/licenses/MIT.

#! FIXME: When running the CLI using two bbmass generated data files execution takes exceedingly long (11+ minutes at minimum)
import argparse
import sys
from typing import Optional, Sequence
from core.td_data_dict import TD_Data_Dictionary, make_dataframe
from core.td_utils import split_dictionary_by_key
import datapane as dp
import pandas as pd

from core.utils import is_csv_file
from extractors.word_level_extractor import WordExtractor

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
    d1 = TD_Data_Dictionary(os.path.join(os.getcwd(), "testdata", "456.csv"))
    d2 = TD_Data_Dictionary(os.path.join(os.getcwd(), "testdata", "789.csv"))
    we = WordExtractor(d1, d2)
    words = we.get_words(d1)
    # print(words)
    dict_splits = split_dictionary_by_key(d1, "key.space")
    print(dict_splits)
    data1 = {
        "Key.shift": "1642214272.327033",
        "'H'": "1642214272.222542",
        "'o'": "1642214272.95212",
        "'f'": "1642214273.212845",
        "'s'": "1642214273.583906",
        "'t'": "1642214273.942847",
        "'r'": "1642214274.183831",
        "'a'": "1642214274.671832",
    }

    data2 = {
        "Key.shift": "1642214275.667853",
        "'R'": "1642214275.5554628",
        "'o'": "1642214275.9677958",
        "'c'": "1642214277.838453",
        "'k'": "1642214276.375573",
        "'s'": "1642214276.4277802",
        "Key.ctrl": "1642214277.422532",
    }
    df = pd.DataFrame(list(data1.items()))
    df2 = pd.DataFrame(list(data2.items()))
    df.columns = ["Keys", "Times"]
    df2.columns = ["Keys", "Times"]
    df["Times"] = df["Times"].astype(float)
    df2["Times"] = df2["Times"].astype(float)
    p1 = df.plot.bar(rot=0)
    p2 = df2.plot.bar(rot=0)
    report = dp.Report(
        dp.Table(
            pd.DataFrame(list(data1.items())),
        ),
        dp.Table(pd.DataFrame(list(data2.items()))),
        dp.Plot(p1, caption="First word"),
        dp.Plot(p2, caption="Second word"),
    )

    report.save(path=os.path.join("reports", "test.html"), open=True)
    # print(dict_splits)


if __name__ == "__main__":
    exit(main())
