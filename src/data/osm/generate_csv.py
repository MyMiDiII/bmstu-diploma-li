import esy.osm.pbf as eop
import numpy as np
import matplotlib.pyplot as plt

from csv_writer import create_csv

def main():
    data = eop.File("./osm/crimean-fed-district-latest.osm.pbf")
    ids = np.sort(np.array([entry.id for entry in data]))

    for order in [10 ** k for k in range(1, 6)]:
        for i in range(1, 10):
            number = i * order
            elements_ids = np.round(np.linspace(0, len(ids) - 1, number)).astype(int)
            ids_set = ids[elements_ids]
            np.random.shuffle(ids_set)
            create_csv("osm", ids_set, number)


if __name__ == "__main__":
    main()
