import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt

from time import process_time_ns


class Lindex:
    def __init__(self, model: tf.keras.Model):
        self.model = model
        self._build_model()

        self.trained = False

    def _build_model(self):
        self.model.compile(optimizer=tf.keras.optimizers.SGD(1e-2),
                           loss=tf.keras.losses.MeanSquaredError(),
                           #loss=tf.keras.losses.MeanAbsoluteError(),
                           metrics=[])

    def _normalize(self, keys):
        min_key = np.min(keys)
        max_key = np.max(keys)
        return (keys - min_key) / (max_key - min_key)

    def train(self, keys: list[int], data: list[any]):
        sort_indexes = np.argsort(keys)

        self.N = len(keys)
        self.keys = np.array(keys)[sort_indexes]
        self.keys = self._normalize(self.keys)
        self.data = np.array(data)[sort_indexes]
        self.positions = np.arange(0, self.N) / self.N

        self.history = self.model.fit(
                self.keys,
                self.positions,
                batch_size=1,
                #callbacks=[LossDiffStop(1e-3)],
                epochs=30)

        self.trained = True

    def plot_history(self):
        if not self.trained:
            return

        print(self.history.history)

    def predict(self, keys):
        if not self.trained:
            return None

        keys = self._normalize(keys)
        pposition = self.model.predict(np.array(keys), verbose=0)
        return np.around(pposition * self.N).astype(int)

    def predict_range(self, low, hight) -> tuple[int, int]:
        pass


if __name__ == "__main__":
    np.random.seed(0)

    size = 100
    keys = np.random.uniform(0, size, size).astype(int)
    #keys = np.random.normal(0.5, 0.16, size)
    #keys = np.random.exponential(2, size)
    #keys = sparce_ids; size = len(keys)
    #print(size)

    values = np.random.randint(0, 100, size)

    # ! RBF

    #initializer = InitCentersRandom(np.array([keys]).T)
    #index = Lindex(RBN(initializer))
    index = Lindex(RBN())
    start = process_time_ns()
    index.train(keys, values)
    rbf_time = process_time_ns() - start
    index.plot_history()

    keys.sort()
    start = process_time_ns()
    ppos = index.predict(keys)
    rbf_ptime = process_time_ns() - start

    positions = np.argsort(keys)
    ppos = ppos.reshape(-1)
    #print(ppos)
    #print(positions)
    errors = dict()
    errors["rbf"] = (np.max(ppos - positions), np.max(positions - ppos))
    I = dict()
    I["rbf"] = sum(errors["rbf"])

    graph(keys, positions, [ppos], ["nn"])

    # ! 3 FCNN

    n = 32
    b = 1 / np.sqrt(n)
    a = -b

    initializer = tf.keras.initializers.RandomUniform(a, b)
    index = Lindex(FCNN([(n, "relu", initializer)] * 3))
    #index = Lindex(FCNN([(n, tf.keras.layers.LeakyReLU(), initializer)] * 3))

    start = process_time_ns()
    index.train(keys, values)
    fcnn_time = process_time_ns() - start
    index.plot_history()

    keys.sort()
    start = process_time_ns()
    ppos = index.predict(keys)
    fcnn_ptime = process_time_ns() - start

    positions = np.argsort(keys)
    ppos = ppos.reshape(-1)
    #print(ppos)
    #print(positions)
    errors["fcnn3"] = (np.max(ppos - positions), np.max(positions - ppos))
    I["fcnn3"] = sum(errors["fcnn3"])

    graph(keys, positions, [ppos], ["nn"])

    # ! FCNN 3 Leaky

    initializer = tf.keras.initializers.RandomUniform(a, b)
    index = Lindex(FCNN([(n, tf.keras.layers.LeakyReLU(), initializer)] * 3))

    start = process_time_ns()
    index.train(keys, values)
    fcnn_l_time = process_time_ns() - start
    index.plot_history()

    keys.sort()
    start = process_time_ns()
    ppos = index.predict(keys)
    fcnn_l_ptime = process_time_ns() - start

    positions = np.argsort(keys)
    ppos = ppos.reshape(-1)
    #print(ppos)
    #print(positions)
    errors["fcnn3l"] = (np.max(ppos - positions), np.max(positions - ppos))
    I["fcnn3l"] = sum(errors["fcnn3l"])

    graph(keys, positions, [ppos], ["nn"])

    # ! 2 FCNN

    index = Lindex(FCNN([(n, "relu", initializer)] * 2))

    start = process_time_ns()
    index.train(keys, values)
    fcnn2_time = process_time_ns() - start
    index.plot_history()

    keys.sort()
    start = process_time_ns()
    ppos = index.predict(keys)
    fcnn2_ptime = process_time_ns() - start

    positions = np.argsort(keys)
    ppos = ppos.reshape(-1)
    #print(ppos)
    #print(positions)
    errors["fcnn2"] = (np.max(ppos - positions), np.max(positions - ppos))
    I["fcnn2"] = sum(errors["fcnn2"])

    graph(keys, positions, [ppos], ["nn"])

    print(errors)
    for key, value in I.items():
        print(key, value)
    print("RBF  ", rbf_time, rbf_ptime)
    print("FCNN3", fcnn_time, fcnn_ptime)
    print("FCNN3 Leaky", fcnn_l_time, fcnn_l_ptime)
    print("FCNN2", fcnn2_time, fcnn2_ptime)
