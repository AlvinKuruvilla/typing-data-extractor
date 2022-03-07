# Copyright 2022, Alvin Kuruvilla <alvineasokuruvilla@gmail.com>

# Use of this source code is governed by an MIT-style
# license that can be found in the LICENSE file or at
# https://opensource.org/licenses/MIT.

# This file is an implementation based on the papers entitled Keyboard Usage Authentication Using Time Series Analysis
# at https://www.researchgate.net/publication/303844583_Keyboard_Usage_Authentication_Using_Time_Series_Analysis
# and Iterative Keystroke Continuous Authentication: A Time Series Based Approach at https://link.springer.com/article/10.1007/s13218-018-0526-z#Sec3
from rich.traceback import install
from typing import List
from numpy import array, zeros, full, argmin, inf
from scipy.spatial.distance import cdist
from math import isinf

install()


def _traceback(D):
    i, j = array(D.shape) - 2
    p, q = [i], [j]
    while (i > 0) or (j > 0):
        tb = argmin((D[i, j], D[i, j + 1], D[i + 1, j]))
        if tb == 0:
            i -= 1
            j -= 1
        elif tb == 1:
            i -= 1
        else:  # (tb == 2):
            j -= 1
        p.insert(0, i)
        q.insert(0, j)
    return array(p), array(q)


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

    def dtw(x, y, dist, warp=1, w=inf, s=1.0):
        """
        Computes Dynamic Time Warping (DTW) of two sequences.
        :param array x: N1*M array
        :param array y: N2*M array
        :param func dist: distance used as cost measure
        :param int warp: how many shifts are computed.
        :param int w: window size limiting the maximal distance between indices of matched entries |i,j|.
        :param float s: weight applied on off-diagonal moves of the path. As s gets larger, the warping path is increasingly biased towards the diagonal
        Returns the minimum distance, the cost matrix, the accumulated cost matrix, and the wrap path.
        """

        assert len(x)
        assert len(y)
        assert isinf(w) or (w >= abs(len(x) - len(y)))
        assert s > 0
        r, c = len(x), len(y)
        if not isinf(w):
            D0 = full((r + 1, c + 1), inf)
            for i in range(1, r + 1):
                D0[i, max(1, i - w) : min(c + 1, i + w + 1)] = 0
            D0[0, 0] = 0
        else:
            D0 = zeros((r + 1, c + 1))
            D0[0, 1:] = inf
            D0[1:, 0] = inf
        D1 = D0[1:, 1:]  # view
        for i in range(r):
            for j in range(c):
                if isinf(w) or (max(0, i - w) <= j <= min(c, i + w)):
                    D1[i, j] = dist(x[i], y[j])
        C = D1.copy()
        jrange = range(c)
        for i in range(r):
            if not isinf(w):
                jrange = range(max(0, i - w), min(c, i + w + 1))
            for j in jrange:
                min_list = [D0[i, j]]
                for k in range(1, warp + 1):
                    i_k = min(i + k, r)
                    j_k = min(j + k, c)
                    min_list += [D0[i_k, j] * s, D0[i, j_k] * s]
                D1[i, j] += min(min_list)
        if len(x) == 1:
            path = zeros(len(y)), range(len(y))
        elif len(y) == 1:
            path = range(len(x)), zeros(len(x))
        else:
            path = _traceback(D0)
        return D1[-1, -1], C, D1, path


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
