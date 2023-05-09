import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt

from time import process_time_ns

from utils.distributions import graph
#from utils.osm import sparce_ids
from indexes.models.fcnn import FCNN
from indexes.models.rbf import *



def min_err(y_true, y_pred):
    return y_pred - y_true

def max_err(y_true, y_pred):
    return y_true - y_pred


class LossDiffStop(tf.keras.callbacks.Callback):
    def __init__(self, diff):
        super().__init__()
        self.diff = diff

    def on_epoch_end(self, epoch, logs=None):
        loss = logs['loss']
        if loss < self.diff:
            self.model.stop_training = True


class Lindex:
    def __init__(self, model: tf.keras.Model):
        self.model = model
        self._build_model()

        self.trained = False

    def _build_model(self):
        self.model.compile(optimizer=tf.keras.optimizers.SGD(1e-2),
                           loss=tf.keras.losses.MeanSquaredError(),
                           #loss=tf.keras.losses.MeanAbsoluteError(),
                           metrics=["accuracy", min_err, max_err])

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

        # print(f"true pos\n {np.where(self.keys == keys[0])}")
        # print(f"bkeys\n {keys}")
        # print(f"bdata\n {data}")
        # print(f"keys\n {self.keys}")
        # print(f"data\n {self.data}")
        # print(f"poss\n {self.positions}")

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
        #plt.plot(self.history.history['min_err'])
        #plt.plot(self.history.history['max_err'])
        plt.plot(self.history.history['accuracy'])
        plt.ylabel('err')
        plt.xlabel('epoch')
        plt.legend(['train'])
        plt.show()

    def predict(self, keys):
        if not self.trained:
            return None
        keys = self._normalize(keys)
        #pposition = int(round(self.model.predict(np.array([[key]]), verbose=0)[0][0]))
        pposition = self.model.predict(np.array(keys), verbose=0)
        return pposition * self.N

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
