import pandas as pd
from typing import List
import collections
from utils import pair_subtract, chunks, m_average, pretty_print


class TDOps():
    def __init__(self):
        pass

    def keys_pressed(self, filepath) -> List[str]:
        res = []
        df = pd.read_csv(filepath)
        keys = df["Key"]
        for key in keys:
            if not (key in res) and key != "'\\x03'":
                res.append(key)
        return res

    def calculate_key_hit_time(self, filepath: str):
        df = pd.read_csv(filepath)
        store = collections.defaultdict(list)
        holder = collections.defaultdict(list)

        hits = collections.defaultdict(int)
        sub_results = collections.defaultdict(list)
        key_occurrences = []
        keys = self.keys_pressed(filepath)
        for key in keys:
            key_occurrences.append(df.loc[df["Key"] == key])
        res = pd.concat(key_occurrences)
        # print(res["Key"].value_counts())
        for i, v in res["Key"].value_counts().items():
            # print('index: ', i, 'value: ', v)
            if v % 2 != 0:
                filtered_res = res[res["Key"] != i]

        # print(store.keys())
        for _, row in filtered_res.iterrows():
            # print(row["Key"], row["Time"])
            store[row["Key"]].append(row["Time"])
            hits[row["Key"]] = 0
        for k, val in store.items():
            # print(k, val)
            if len(val) == 2:
                hits[k] = val[1] - val[0]
            # print(k, val)
        for a, b in hits.items():
            if b > 0:
                del_value = store.pop(a)
                holder[a] = del_value
        for c, d in store.items():
            ch = chunks(d, 2)
            for p in ch:
                sub_results[c].append(pair_subtract(p))
        for l, m in sub_results.items():
            #print(l, m)
            store[l] = m_average(m)
        for x, y in holder.items():
            #print(x, y)
            store[x] = pair_subtract(y)
        pretty_print(store)
        return store

    def calculate_key_interval_time(self, filepath: str):
        df = pd.read_csv(filepath)
        operation = df["Press or Release"]
        op_counter = 0
        for i in operation:
            print(i)
        pass
