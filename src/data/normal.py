import numpy as np

from csv_writer import choose_elements

def generate_normal():
    size = 100000000
    ids = np.random.normal(size / 2, size / 10, size).astype(int)

    choose_elements("normal", ids)


if __name__ == "__main__":
    generate_normal()
