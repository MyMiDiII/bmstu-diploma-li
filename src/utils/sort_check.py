import numpy as np

from time import process_time_ns

np_a = np.random.randint(0, 100000, size=100000)
a = list(np_a)

start = process_time_ns()
np_a.sort()
finish = process_time_ns()

print(f"{finish - start} ns for numpy")

start = process_time_ns()
a.sort()
finish = process_time_ns()

print(f"{finish - start} ns for python")
