import csv
import numpy as np


def load_keys(filename, size):
    keys = np.memmap("keys.dat", dtype='int64', mode='w+', shape=(size,))
    with open(filename, "r", newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        _ = next(reader)
        for i, row in enumerate(reader):
            keys[i] = int("".join(row))

    print(keys)

    return keys

