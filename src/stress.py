# Copyright 2022, Alvin Kuruvilla <alvineasokuruvilla@gmail.com>

# Use of this source code is governed by an MIT-style
# license that can be found in the LICENSE file or at
# https://opensource.org/licenses/MIT.

from core.td_data_dict import TD_Data_Dictionary
from rich.traceback import install
import os
from extractors.word_level_extractor import WordExtractor

install()


def main():
    d1 = TD_Data_Dictionary(os.path.join(os.getcwd(), "testdata", "456.csv"))
    d2 = TD_Data_Dictionary(os.path.join(os.getcwd(), "testdata", "789.csv"))
    we = WordExtractor(d1, d2)
    words = we.get_words(d1)
    print(words)


if __name__ == "__main__":
    main()
