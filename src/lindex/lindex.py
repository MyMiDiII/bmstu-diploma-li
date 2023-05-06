import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt

from utils.distributions import graph

class PredictionCallback(tf.keras.callbacks.Callback):
    def on_epoch_begin(self, epoch, logs=None):
        # Get the predicted values for the input data
        print(logs)


class Lindex:
    def __init__(self, keys: list[int], data: list[any]):
        sort_indexes = np.argsort(keys)

        self.N = len(keys)
        self.keys = np.array(keys)[sort_indexes]
        self.data = np.array(data)[sort_indexes]
        self.positions = np.arange(0, self.N) / self.N

        # print(f"true pos\n {np.where(self.keys == keys[0])}")
        # print(f"bkeys\n {keys}")
        # print(f"bdata\n {data}")
        print(f"keys\n {self.keys}")
        # print(f"data\n {self.data}")
        print(f"poss\n {self.positions}")

        self.model = self._build_model()
        self.model.summary()

    def _build_model(self):
        n = 32
        b = 1 / np.sqrt(n)
        a = -b
        initializer = tf.keras.initializers.RandomUniform(a, b)
        model = tf.keras.models.Sequential([
            tf.keras.layers.Dense(32,
                                  activation="relu",
                                  kernel_initializer=initializer,
                                  bias_initializer=initializer,
                                  input_dim=1),
            tf.keras.layers.Dense(32,
                                  activation="relu",
                                  kernel_initializer=initializer,
                                  bias_initializer=initializer),
            tf.keras.layers.Dense(1)
            ])
        model.compile(optimizer=tf.keras.optimizers.SGD(0.001),
                      loss=tf.keras.losses.MeanSquaredError())

        return model

    def train(self):

        history = self.model.fit(
                self.keys,
                self.positions,
                batch_size=1,
                callbacks=[PredictionCallback()],
                epochs=100)

        print(history.history)
        plt.plot(history.history['loss'])
        plt.ylabel('loss')
        plt.xlabel('epoch')
        plt.legend(['train'])
        plt.show()

    def predict(self, key: int) -> int:
        #pposition = int(round(self.model.predict(np.array([[key]]), verbose=0)[0][0]))
        pposition = self.model.predict(np.array([key]), verbose=0)[0][0]
        return pposition * self.N

    def predict_range(self, low, hight) -> tuple[int, int]:
        pass


if __name__ == "__main__":
    np.random.seed(0)

    size = 100
    keys = np.random.uniform(0, 1, size)
    values = np.random.randint(0, 100, size)

    index = Lindex(keys, values)
    index.train()

    keys.sort()
    ppos = [index.predict(key) for key in keys]
    print(list(zip(keys, ppos)))

    graph(keys, np.argsort(keys), [ppos], ["nn"])
