import sys
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt

from time import process_time_ns

from indexes.metrics import MetricsCallback

from timer import timer

from utils.keras_memory_usage import keras_model_memory_usage_in_bytes

class Lindex:
    def __init__(self, model: tf.keras.Model):
        self.model = model
        self._build_model()

        self.trained = False
        #print("build ok");

        self.statistics = {}


    def _build_model(self):
        self.model.compile(optimizer=tf.keras.optimizers.SGD(1e-2),
                           loss=tf.keras.losses.MeanSquaredError(),
                           #loss=tf.keras.losses.MeanAbsoluteError(),
                           metrics=[])

    def _normalize(self, keys):
        if keys.size == 0:
            return

        min_key = np.min(self.keys)
        max_key = np.max(self.keys)
        return (keys - min_key) / (max_key - min_key)

    def _init_for_train(self, keys: list[int], data: list[any]):
        sort_indexes = np.argsort(keys)

        self.N = len(keys)
        self.keys = np.array(keys)[sort_indexes]
        self.norm_keys = self._normalize(self.keys)
        self.data = np.array(data)[sort_indexes]
        self.positions = np.arange(0, self.N) / (self.N - 1)

    def _true_train(self):
        self.history = self.model.fit(
                self.norm_keys,
                self.positions,
                batch_size=1,
                #callbacks=[LossDiffStop(1e-3)],
                callbacks=[self.metrics],
                epochs=30)

    @timer
    def train(self, keys: list[int], data: list[any]):
        self._init_for_train(keys, data)

        self.metrics = MetricsCallback(self.norm_keys, self.positions)

        self._true_train()

        self.trained = True

    def plot_history(self):
        if not self.trained:
            return

        #print(self.history.history)

    def _predict(self, keys):
        if not self.trained:
            return None

        #print(keys)
        keys = self._normalize(keys)
        pposition = self.model.predict(keys, verbose=0)
        return np.around(pposition * self.N).astype(int).reshape(-1)

    def _clarify(self, keys, positions):
        def clarify_one(key, position):
            position = max(min(position, self.N - 1), 0)

            if self.keys[position] == key:
                return position

            low = max(position - self.metrics.mean_absolute_error, 0)
            high = min(position + self.metrics.mean_absolute_error, self.N - 1)

            if not (self.keys[low] < key < self.keys[high]):
                low = max(position - self.metrics.max_absolute_error, 0)
                high = min(position + self.metrics.max_absolute_error, self.N - 1)

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
        return vec_clarify(keys, positions)

    @timer
    def find(self, keys):
        #print("called")
        if not self.trained or not keys:
            return None

        #print("in keys", keys)
        keys = np.array(keys)
        positions = self._predict(keys)
        positions = self._clarify(keys, positions)
        #print("res", self.data[positions])
        return self.data[positions]

    def predict_range(self, low, hight) -> tuple[int, int]:
        pass

    def is_trained(self):
        return self.is_trained

    def my_size(self):
        size = 0
        attributes = vars(self)

        for attr_name, attr_value in attributes.items():
            if attr_name == "model":
                size += keras_model_memory_usage_in_bytes(attr_value, batch_size=32)
            if attr_name not in ["statistics", "metrics", "history"]:
                if isinstance(attr_value, np.ndarray):
                    size += attr_value.nbytes
                else:
                    size += sys.getsizeof(attr_value)

        return size

    def mae(self):
        return self.metrics.mean_absolute_error;

