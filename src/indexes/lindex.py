import sys
import os
import pickle

import numpy as np
import matplotlib.pyplot as plt

from time import process_time_ns

from indexes.models.abs_model import AbstractModel

from utils.timer import timer


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
        sort_indexes = np.argsort(keys)

        self.N = len(keys)
        self.keys = np.array(keys)[sort_indexes]
        self.norm_keys = self._normalize(self.keys)
        self.data = np.array(data)[sort_indexes]
        self.positions = np.arange(0, self.N) / (self.N - 1)

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

    #@profile
    def _predict(self, keys):
        if not self.trained:
            return None

        keys = self._normalize(keys)
        pposition = self.model(keys)
        return np.around(pposition * self.N).astype(int).reshape(-1)

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
        return positions[positions >= 0]

    @timer
    def find(self, keys):
        if not self.trained or not keys:
            return None

        keys = np.array(keys)
        positions = self._predict(keys)
        positions = self._clarify(keys, positions)
        return self.data[positions]

    def insert(self, key, data):
        index = np.searchsorted(self.keys, key)
        self.keys = np.insert(self.keys, index, key)
        self.data = np.insert(self.data, index, data)
        self.N = len(self.keys)

        self._true_train()

    def predict_range(self, low, hight) -> tuple[int, int]:
        pass

    def is_trained(self):
        return self.trained

    def my_size(self):
        size = 0
        attributes = vars(self)

        for attr_name, attr_value in attributes.items():
            if attr_name == "model":
                size += attr_value.size()
            if attr_name not in ["statistics", "metrics", "history"]:
                if isinstance(attr_value, np.ndarray):
                    size += attr_value.nbytes
                else:
                    size += sys.getsizeof(attr_value)

        return size

    def mae(self):
        return self.mean_abs_err

    def save_model(self, path):
        self.model.save(f"{path}/model")

        index = {
                "keys" : self.keys,
                "data" : self.data,
                "positions" : self.positions,
                "max_ae" : self.max_abs_err,
                "mean_ae" : self.mean_abs_err,
                "trained" : self.trained
                }

        with open(f"{path}/data.pickle", "wb") as f:
            pickle.dump(index, f)

