import csv


def load_keys(filename):
    keys = []
    with open(filename, "r", newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        _ = next(reader)
        for row in reader:
            keys.append(int("".join(row)))

    return keys

