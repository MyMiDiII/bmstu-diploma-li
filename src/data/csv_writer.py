import csv

def create_csv(prefix, keys, elements_number):
    with open(f"csv/{prefix}/{prefix}{elements_number}.csv",
              "w", newline="") as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        writer.writerow(["ids"])

        for key in keys:
            writer.writerow([key])
