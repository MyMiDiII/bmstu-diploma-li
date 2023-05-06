import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt

from utils.distributions import graph

class LossDiffStop(tf.keras.callbacks.Callback):
    def __init__(self, diff):
        super().__init__()
        self.diff = diff

    def on_epoch_end(self, epoch, logs=None):
        loss = logs['loss']
        if loss < self.diff:
            self.model.stop_training = True


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
        model.compile(optimizer=tf.keras.optimizers.SGD(0.01),
                      loss=tf.keras.losses.MeanSquaredError())

        return model

    def train(self):

        history = self.model.fit(
                self.keys,
                self.positions,
                batch_size=1,
                callbacks=[LossDiffStop(1e-4)],
                epochs=60)

        print(history.history)
        plt.plot(history.history['loss'])
        plt.ylabel('loss')
        plt.xlabel('epoch')
        plt.legend(['train'])
        plt.show()

    def predict(self, keys):
        #pposition = int(round(self.model.predict(np.array([[key]]), verbose=0)[0][0]))
        pposition = self.model.predict(np.array(keys), verbose=0)
        return pposition * self.N

    def predict_range(self, low, hight) -> tuple[int, int]:
        pass


if __name__ == "__main__":
    np.random.seed(0)

    size = 1000
    #keys = np.random.uniform(0, 1, size)
    keys = np.random.normal(0.5, 0.16, size)
    #keys = np.random.exponential(2, size)
    values = np.random.randint(0, 100, size)

    index = Lindex(keys, values)
    index.train()

    keys.sort()
    ppos = index.predict(keys)

    graph(keys, np.argsort(keys), [ppos], ["nn"])
