from core.td_data_dict import TD_Data_Dictionary
from extractors.word_level_extractor import WordExtractor
import os
from rich.traceback import install

install()


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


def test_get_words():
    d1 = TD_Data_Dictionary(os.path.join(os.getcwd(), "testdata", "456.csv"))
    d2 = TD_Data_Dictionary(os.path.join(os.getcwd(), "testdata", "789.csv"))
    we = WordExtractor(d1, d2)
    words = we.get_words(d1)
    words2 = we.get_words(d2)
    assert len(words) == 2
    assert len(words2) == 2
