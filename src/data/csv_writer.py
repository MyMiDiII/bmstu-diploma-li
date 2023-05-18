import csv
import numpy as np

def create_csv(prefix, keys, elements_number):
    with open(f"csv/{prefix}/{prefix}{elements_number}.csv",
              "w", newline="") as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        writer.writerow(["keys"])

        for key in keys:
            writer.writerow([key])


def choose_elements(prefix, keys):
    keys = np.sort(keys)
    for order in [10 ** k for k in range(1, 6)]:
        print(f"ORDER {order}")
        for i in range(1, 10):
            number = i * order
            elements_keys = np.round(np.linspace(0, len(keys) - 1, number)).astype(int)
            keys_set = keys[elements_keys]
            np.random.shuffle(keys_set)
            create_csv(prefix, keys_set, number)
