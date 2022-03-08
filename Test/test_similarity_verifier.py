# Copyright 2022, Alvin Kuruvilla <alvineasokuruvilla@gmail.com>

# Use of this source code is governed by an MIT-style
# license that can be found in the LICENSE file or at
# https://opensource.org/licenses/MIT.

from core.td_data_dict import TD_Data_Dictionary
import os
from verifiers.similarity_verifier import SimilarityVerifier


def test_get_template():
    d1 = TD_Data_Dictionary(os.path.join(os.getcwd(), "testdata", "456.csv"))
    d2 = TD_Data_Dictionary(os.path.join(os.getcwd(), "testdata", "789.csv"))
    sim_verifier = SimilarityVerifier(d1.path(), d2.path(), 2.0)
    assert sim_verifier.template_path() == d1.path()


def test_get_verification():
    d1 = TD_Data_Dictionary(os.path.join(os.getcwd(), "testdata", "456.csv"))
    d2 = TD_Data_Dictionary(os.path.join(os.getcwd(), "testdata", "789.csv"))
    sim_verifier = SimilarityVerifier(d1.path(), d2.path(), 2.0)
    assert sim_verifier.verification_path() == d2.path()


def test_get_threshold():
    d1 = TD_Data_Dictionary(os.path.join(os.getcwd(), "testdata", "456.csv"))
    d2 = TD_Data_Dictionary(os.path.join(os.getcwd(), "testdata", "789.csv"))
    sim_verifier = SimilarityVerifier(d1.path(), d2.path(), 2.0)
    assert sim_verifier.get_threshold() == 2.0


def test_set_template_file_path():
    d1 = TD_Data_Dictionary(os.path.join(os.getcwd(), "testdata", "456.csv"))
    d2 = TD_Data_Dictionary(os.path.join(os.getcwd(), "testdata", "789.csv"))
    sim_verifier = SimilarityVerifier(d1.path(), d2.path(), 2.0)
    sim_verifier.set_template_file_path(
        os.path.join(os.getcwd(), "Test", "sources", "single-entry-verification.csv")
    )
    assert sim_verifier.template_path() == os.path.join(
        os.getcwd(), "Test", "sources", "single-entry-verification.csv"
    )


def test_set_verification_file_path():
    d1 = TD_Data_Dictionary(os.path.join(os.getcwd(), "testdata", "456.csv"))
    d2 = TD_Data_Dictionary(os.path.join(os.getcwd(), "testdata", "789.csv"))
    sim_verifier = SimilarityVerifier(d1.path(), d2.path(), 2.0)
    sim_verifier.set_verification_file_path(
        os.path.join(os.getcwd(), "Test", "sources", "single-entry-verification.csv")
    )
    assert sim_verifier.verification_path() == os.path.join(
        os.getcwd(), "Test", "sources", "single-entry-verification.csv"
    )
