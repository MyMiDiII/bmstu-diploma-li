import numpy as np


class Lindex:
    def __init__(self, keys: list[int], data: list[any]):
        sort_indexes = np.argsort(keys)

        self.keys = np.array(keys)[sort_indexes]
        self.data = np.array(data)[sort_indexes]
        self.positions = np.arange(0, len(self.keys))

    def _build_model(self):
        pass

    def train(self):
        pass

    def predict(self, key: int) -> int:
        pass

    def predict_range(self, low, hight) -> tuple[int, int]:
        pass


if __name__ == "__main__":
    size = 3
    keys = np.random.uniform(0, 10000, size).astype(int)
    values = np.random.randint(0, 1000, size)

    index = Lindex(keys, values)
