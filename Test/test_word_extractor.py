from core.td_data_dict import TD_Data_Dictionary
from extractors.word_level_extractor import WordExtractor
import os


def test_get_template():
    d1 = TD_Data_Dictionary(os.path.join(os.getcwd(), "testdata", "456.csv"))
    d2 = TD_Data_Dictionary(os.path.join(os.getcwd(), "testdata", "789.csv"))
    we = WordExtractor(d1, d2)
    assert we.get_template().data() == d1.data()


# String Split - Splits a string to two substrings
def test_get_verification():
    d1 = TD_Data_Dictionary(os.path.join(os.getcwd(), "testdata", "456.csv"))
    d2 = TD_Data_Dictionary(os.path.join(os.getcwd(), "testdata", "789.csv"))
    we = WordExtractor(d1, d2)
    assert we.get_verification().data() == d2.data()


def test_setters():
    # For this I think we can use parameters in the test functions like this:
    # nose2.tools import params
    # @params("Sir Bedevere", "Miss Islington", "Duck")
    # def test_is_knight(value):
    # assert value.startswith('Sir')
    #
    # See https://pypi.org/project/nose2/

    pass
