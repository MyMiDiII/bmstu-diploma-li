import esy.osm.pbf as eop
import numpy as np
import matplotlib.pyplot as plt

print("FILE")
data = eop.File("../data/crimean-fed-district-latest.osm.pbf")

print("LOAD")
ids = np.sort(np.array([entry.id for entry in data]))
positions = np.arange(len(ids))

sparce_ids = ids[::1000]
sparce_positions = positions[::1000]

print(len(sparce_ids))

print("PRINT")
plt.plot(sparce_ids, sparce_positions)
plt.show()


