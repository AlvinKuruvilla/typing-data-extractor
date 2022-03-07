from core.td_data_dict import TD_Data_Dictionary
import os
from rich.traceback import install

from verifiers.similarity_verifier import SimilarityVerifier

install()


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
