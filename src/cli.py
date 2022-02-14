# Copyright 2022, Alvin Kuruvilla <alvineasokuruvilla@gmail.com>

# Use of this source code is governed by an MIT-style
# license that can be found in the LICENSE file or at
# https://opensource.org/licenses/MIT.

#! FIXME: When running the CLI using two bbmass generated data files execution takes exceedingly long (11+ minutes at minimum)
import argparse
import sys
from typing import Optional, Sequence
from core.td_data_dict import TD_Data_Dictionary, make_dataframe

# from verifiers.absolute_verifier import AbsoluteVerifier
from core.utils import is_csv_file
from verifiers.reporter import DataReporter

# from verifiers.similarity_verifier import SimilarityVerifier
from verifiers.relative_verifier import RelativeVerifier
from rich.traceback import install
from verifiers.verifier_utils import (
    find_matching_interval_keys,
    dataframe_from_list,
    find_matching_keys,
    compress_interval,
)

# from verifiers.evaluator import Verifier_Evaluator, validate_verifier_type
import datapane as dp
import os
import pandas as pd

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
    data_dict = TD_Data_Dictionary(input_path)
    pairs = data_dict.get_key_pairs()
    # print(data_dict.calculate_key_interval_time(pairs))

    comp_dict = TD_Data_Dictionary(other_path)
    # data_dict.calculate_key_hold_time()

    # print(find_matching_keys(input_path, other_path))
    r_verifier = RelativeVerifier(input_path, other_path, 1.0)
    r_verifier.find_all_valid_keys()
    interval_matches = find_matching_interval_keys(input_path, other_path)
    regular_matches = find_matching_keys(input_path, other_path)
    # print(r_verifier.find_all_valid_keys())
    # print(matches)
    # eval = Verifier_Evaluator(r_verifier, 0.50)
    # a, b = eval.extract_features()
    # print("Hello ", *eval.evaluate(a, b))
    reporter = DataReporter()
    template_df = make_dataframe(data_dict)
    verification_df = make_dataframe(comp_dict)
    source = r_verifier.get_valid_keys_data()
    print("Source:", source)
    plot_keys = list(source.keys())
    plot_values = list(source.values())
    keys_df = dataframe_from_list(plot_keys, ["Keys"])
    values_df = dataframe_from_list(plot_values, ["Times"])
    df = pd.concat([keys_df, values_df], axis=1)
    # print(df)
    ax = df.plot.bar(x="Keys", y="Times", rot=0)
    # print(ax)

    report = dp.Report(
        dp.DataTable(template_df, caption=f"Template Data"),
        dp.DataTable(verification_df, caption=f"Verification Data"),
        dp.DataTable(
            dataframe_from_list(regular_matches, ["Keys"]),
            caption="Matching Keys",
        ),
        dp.DataTable(
            dataframe_from_list(compress_interval(interval_matches), ["Keys"]),
            caption="Matching Interval Keys",
        ),
        dp.Plot(ax, caption=r_verifier.class_name()),
    )
    report.save(path=os.path.join(reporter.get_report_path(), "test.html"), open=True)


if __name__ == "__main__":
    exit(main())
