import esy.osm.pbf as eop
import numpy as np
import matplotlib.pyplot as plt

print("FILE")
data = eop.File("./crimean-fed-district-latest.osm.pbf")

print("LOAD")
ids = np.sort(np.array([entry.id for entry in data]))
positions = np.arange(len(ids))

sparce_ids = ids[::10000]
sparce_positions = positions[::10000]

print(len(sparce_ids))

print("PRINT")
plt.plot(sparce_ids, sparce_positions)
plt.show()


