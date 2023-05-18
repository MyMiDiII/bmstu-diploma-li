import esy.osm.pbf as eop
import numpy as np

from csv_writer import choose_elements

def generate_osm():
    data = eop.File("./osm/crimean-fed-district-latest.osm.pbf")
    ids = np.sort(np.array([entry.id for entry in data]))

    choose_elements("osm", ids)

if __name__ == "__main__":
    generate_osm()
