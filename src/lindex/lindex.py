import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt


class Lindex:
    def __init__(self, keys: list[int], data: list[any]):
        sort_indexes = np.argsort(keys)

        self.keys_sort = np.array(keys)[sort_indexes]
        self.data_sort = np.array(data)[sort_indexes]
        self.positions_sort = np.arange(0, len(self.keys_sort))

        self.keys = np.array(keys)
        self.data = np.array(data)
        self.positions = np.argsort(keys)

        # print(f"true pos\n {np.where(self.keys == keys[0])}")
        # print(f"bkeys\n {keys}")
        # print(f"bdata\n {data}")
        # print(f"keys\n {self.keys}")
        # print(f"data\n {self.data}")
        # print(f"poss\n {self.positions}")

        self.model = self._build_model()
        self.model_sort = self._build_model()
        self.model.summary()

    def _build_model(self):
        model = tf.keras.models.Sequential([
            tf.keras.layers.Dense(64, activation="relu", input_dim=1),
            tf.keras.layers.Dense(64, activation="relu"),
            tf.keras.layers.Dense(1, activation="linear")
            ])
        model.compile(loss='mean_squared_error')

        print(model)

        return model

    def train(self):
        history = self.model_sort.fit(self.keys_sort, self.positions_sort,
                                 epochs=500,
                                 verbose=0)

        plt.plot(history.history['loss'])
        plt.title('model loss')
        plt.ylabel('loss')
        plt.xlabel('epoch')
        plt.legend(['train'], loc='upper left')
        plt.show()

        self.model_sort.summary()

        history = self.model.fit(self.keys, self.positions,
                                 epochs=500,
                                 verbose=0)

        plt.plot(history.history['loss'])
        plt.title('model loss')
        plt.ylabel('loss')
        plt.xlabel('epoch')
        plt.legend(['train'], loc='upper left')
        plt.show()

        self.model.summary()

    def predict(self, key: int) -> int:
        pposition_sort = int(round(self.model_sort.predict(np.array([[key]]), verbose=0)[0][0]))
        pposition = int(round(self.model.predict(np.array([[key]]), verbose=0)[0][0]))
        return pposition_sort, pposition

    def predict_range(self, low, hight) -> tuple[int, int]:
        pass


if __name__ == "__main__":
    np.random.seed(0)

    size = 1000
    keys = np.random.uniform(0, 10000, size).astype(int)
    values = np.random.randint(0, 1000, size)

    key = keys[0]
    index = Lindex(keys, values)
    index.train()
    index.predict(key)

    print(f"pkey {key}")
