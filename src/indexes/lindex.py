import sys
import os
import pickle

import numpy as np
import matplotlib.pyplot as plt

from time import process_time_ns

from indexes.models.abs_model import AbstractModel

from utils.timer import timer

#from line_profiler import LineProfiler

class Lindex:
    def __init__(self, model: AbstractModel):
        self.model = model
        self.model.build()

        self.trained = False

        self.max_abs_err = 0
        self.mean_abs_err = 0

    def _normalize(self, keys):
        if keys.size == 0:
            return

        min_key = self.keys[0]
        max_key = self.keys[-1]
        return (keys - min_key) / (max_key - min_key)

    #@profile
    def _init_for_train(self, keys: list[int], data: list[any]):
        print("SORT")
        sort_indexes = np.argsort(keys)

        self.N = len(keys)
        size = self.N
        print("KEYS")
        self.keys = np.memmap(f"keys{self.N}.dat", dtype='int64',
                              mode='w+', shape=(size, ))
        np.copyto(self.keys, np.array(keys)[sort_indexes])
        #self.keys = np.array(keys)[sort_indexes]
        print("NORM")
        self.norm_keys = np.memmap(f"norm_keys{self.N}.dat", dtype='float32',
                              mode='w+', shape=(size, ))
        np.copyto(self.norm_keys, self._normalize(self.keys))
        #self.norm_keys = self._normalize(self.keys)
        #self.data = np.array(data)[sort_indexes]
        print("POS")
        self.positions = np.memmap(f"pos{self.N}.dat", dtype='float32',
                              mode='w+', shape=(size, ))
        np.copyto(self.positions, np.arange(0, self.N) / (self.N - 1))
        #self.positions = np.arange(0, self.N) / (self.N - 1)

    #@profile
    def _true_train(self):
        self.model.train(self.norm_keys, self.positions)

    @timer
    #@profile
    def train(self, keys: list[int], data: list[any]):
        self._init_for_train(keys, data)

        self._true_train()

        self.mean_abs_err = self.model.get_mean_abs_err()
        self.max_abs_err = self.model.get_max_abs_err()

        self.trained = True

    @timer
    #@profile
    def _predict(self, keys):
        if not self.trained:
            return None

        keys = self._normalize(keys)
        pposition = self.model(keys)
        return np.around(pposition * self.N).astype(int).reshape(-1)

    @timer
    #@profile
    def _clarify(self, keys, positions):
        def clarify_one(key, position):
            position = max(min(position, self.N - 1), 0)

            if self.keys[position] == key:
                return position

            low = max(position - self.mean_abs_err, 0)
            high = min(position + self.mean_abs_err, self.N - 1)

            if not (self.keys[low] < key < self.keys[high]):
                low = max(position - self.max_abs_err, 0)
                high = min(position + self.max_abs_err, self.N - 1)

            while low <= high:
                mid = (low + high) // 2
                if self.keys[mid] == key:
                    return mid
                elif self.keys[mid] < key:
                    low = mid + 1
                else:
                    high = mid - 1

            return -1

        vec_clarify = np.vectorize(clarify_one)
        positions = vec_clarify(keys, positions)
        #print("POS ALL", positions)
        return positions[positions >= 0]

    @timer
    #@profile
    def find(self, keys):
        if not self.trained or not keys:
            return None

        keys = np.array(keys)
        #print("SELF KEYS", self.keys)
        positions, predict_time = self._predict(keys)
        #print("POS NOT CLARIFY", positions)
        positions, clarify_time = self._clarify(keys, positions)

        #print("DATA", self.data[positions])

        #return self.data[positions], predict_time, clarify_time
        return positions, predict_time, clarify_time

    def insert(self, key, data):
        index = np.searchsorted(self.keys, key)
        self.keys = np.insert(self.keys, index, key)
        self.data = np.insert(self.data, index, data)
        self.N = len(self.keys)

        self._true_train()

    def _range_binsearch(self, key, lower, upper):
        while lower <= upper:
            mid = (lower + upper) // 2
            if self.keys[mid] == key:
                return mid, mid
            elif self.keys[mid] < key:
                lower = mid + 1
            else:
                upper = mid - 1

        return min(lower, upper), max(lower, upper)

    def _range_clarify(self, key, limit, is_lower, constraint):
        if is_lower and np.isnan(limit):
            return 0
        elif np.isnan(limit):
            return self.N - 1

        key = int(key)
        limit = int(limit)

        limit = max(min(limit, self.N - 1), 0)

        lower, upper = limit, limit

        if self.keys[limit] != key:
            bin_lower = max(limit - self.mean_abs_err, 0)
            bin_upper = min(limit + self.mean_abs_err, self.N - 1)

            if not (self.keys[bin_lower] < key < self.keys[bin_upper]):
                bin_lower = max(limit - self.max_abs_err, 0)
                bin_upper = min(limit + self.max_abs_err, self.N - 1)

            lower, upper = self._range_binsearch(key, bin_lower, bin_upper)

        #print("_range_clarify")
        #print(lower, upper)

        if lower == upper:
            #print(is_lower)
            #print(int(is_lower))
            #print(constraint)
            #print((-1) ** int(is_lower) * constraint)
            return lower - (-1) ** int(is_lower) * constraint

        if is_lower:
            return upper

        return lower

    @timer
    def predict_range(self, keys_range, constraint):
        if keys_range[0] is not None and keys_range[1] is not None:
            if keys_range[0] > keys_range[1]:
                keys_range[0], keys_range[1] = keys_range[1], keys_range[0]
                constraint[0], constraint[1] = constraint[1], constraint[0]

        keys_range = np.array([np.nan if x is None else x for x in keys_range])

        positions_limits = self._predict(keys_range)
        positions_limits = positions_limits.astype(float)
        positions_limits[np.isnan(keys_range)] = np.nan
        #print(positions_limits)

        lower = self._range_clarify(keys_range[0], positions_limits[0], True,
                              constraint[0])
        upper = self._range_clarify(keys_range[1], positions_limits[1], False,
                              constraint[1])

        #print(lower, upper)

        return self.data[lower:upper + 1]


    def is_trained(self):
        return self.trained

    def my_sizes(self):
        size = 0
        attributes = vars(self)
        model_size = 0

        for attr_name, attr_value in attributes.items():
            if attr_name == "model":
                #print(attr_name)
                model_size = attr_value.size()
                size += model_size
            if attr_name not in ["statistics",
                                 "metrics",
                                 "history",
                                 "positions",
                                 "N",
                                 "norm_keys",
                                 "trained"]:
                #print(attr_name)
                if isinstance(attr_value, np.ndarray):
                    size += attr_value.nbytes
                else:
                    size += sys.getsizeof(attr_value)

        return size, model_size

    def mean_ae(self):
        return self.mean_abs_err

    def max_ae(self):
        return self.max_abs_err

    def save_model(self, path):
        self.model.save(f"{path}/model")

        index = {
                "keys" : self.keys,
                #"data" : self.data,
                "positions" : self.positions,
                "max_ae" : self.max_abs_err,
                "mean_ae" : self.mean_abs_err,
                "trained" : self.trained
                }

        with open(f"{path}/data.pickle", "wb") as f:
            pickle.dump(index, f)

