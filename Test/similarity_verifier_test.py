from core.td_data_dict import TD_Data_Dictionary
import os
from rich.traceback import install

install()


def test_get_template():
    d1 = TD_Data_Dictionary(os.path.join(os.getcwd(), "testdata", "456.csv"))
    d2 = TD_Data_Dictionary(os.path.join(os.getcwd(), "testdata", "789.csv"))
