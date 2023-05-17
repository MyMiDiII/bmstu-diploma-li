import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt

from time import process_time_ns

from indexes.metrics import MetricsCallback

class Lindex:
    def __init__(self, model: tf.keras.Model):
        self.model = model
        self._build_model()

        self.trained = False
        print("build ok");


    def _build_model(self):
        self.model.compile(optimizer=tf.keras.optimizers.SGD(1e-2),
                           loss=tf.keras.losses.MeanSquaredError(),
                           #loss=tf.keras.losses.MeanAbsoluteError(),
                           metrics=[])

    def _normalize(self, keys):
        min_key = np.min(self.keys)
        max_key = np.max(self.keys)
        return (keys - min_key) / (max_key - min_key)

    def train(self, keys: list[int], data: list[any]):
        print("train")
        sort_indexes = np.argsort(keys)

        self.N = len(keys)
        self.keys = np.array(keys)[sort_indexes]
        self.norm_keys = self._normalize(self.keys)
        self.data = np.array(data)[sort_indexes]
        self.positions = np.arange(0, self.N) / self.N

        self.metrics = MetricsCallback(self.norm_keys, self.positions)

        self.history = self.model.fit(
                self.norm_keys,
                self.positions,
                batch_size=1,
                #callbacks=[LossDiffStop(1e-3)],
                callbacks=[self.metrics],
                epochs=30)

        self.trained = True

    def plot_history(self):
        if not self.trained:
            return

        print(self.history.history)

    def _predict(self, keys):
        if not self.trained:
            return None

        #print(keys)
        keys = self._normalize(keys)
        pposition = self.model.predict(np.array(keys), verbose=0)
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

    def find(self, keys):
        if not self.trained:
            return None

        positions = self._predict(keys)
        return self._clarify(keys, positions)


    def predict_range(self, low, hight) -> tuple[int, int]:
        pass

