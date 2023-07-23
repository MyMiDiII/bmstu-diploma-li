import numpy as np

from csv_writer import choose_elements

def generate_uniform():
    size = 100000000
    ids = np.random.uniform(0, size * 10, size).astype(int)

    choose_elements("uniform", ids)


if __name__ == "__main__":
    generate_uniform()
