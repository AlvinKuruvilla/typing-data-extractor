# Copyright 2022, Alvin Kuruvilla <alvineasokuruvilla@gmail.com>

# Use of this source code is governed by an MIT-style
# license that can be found in the LICENSE file or at
# https://opensource.org/licenses/MIT.

# This file is an implementation based on the papers entitled Keyboard Usage Authentication Using Time Series Analysis
# at https://www.researchgate.net/publication/303844583_Keyboard_Usage_Authentication_Using_Time_Series_Analysis
# and Iterative Keystroke Continuous Authentication: A Time Series Based Approach at https://link.springer.com/article/10.1007/s13218-018-0526-z#Sec3
from rich.traceback import install
from typing import List

install()


class Feature_Set:
    """The set of keystroke features for a specific `Point`

    A `Feature_Set' contains an array where the first element is the key and the second element is the associated KHT
    """

    # If we add more features we can just add new getters for them and add them to the constructor.
    # We may also want to ecplore Optional arguments, so a Feature_Set can be constructed with one or more features,
    # but at minimum only needs one
    def __init__(self, kht_feature):
        self.kht_feature = kht_feature

    def get_kht_feature(self):
        return self.kht_feature

    def get_key(self):
        return self.kht_feature[0]

    def get_KHT_value(self):
        return self.kht_feature[1]


class Point:
    """A Point consists of 2 elements:
    1) The timestamp at which the key was pressed
    2) Feature Set: The set of keystroke features for that key
    """

    def __init__(self, timestamp, feature_set: Feature_Set):
        self.timestamp = timestamp
        self.feature_set = feature_set

    def timestamp(self):
        return self.timestamp

    def feature_set(self):
        return self.feature_set


class Keystroke_Time_Series:
    """A Keystroke Time Series is a sequence of data points, P, which has a length.

    Each point is a class consisting of several keystroke features

    See `Feature_Set`
    """

    def __init__(self, sequence: List[Point]):
        self.sequence = sequence

    def length(self):
        return len(self.sequence)
