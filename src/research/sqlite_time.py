import os
import sqlite3
import csv
import time
import subprocess
import pandas as pd

CSV_PATH = "research/csv_res/"

SIZES = []
SIZES += [10 ** 4 * i for i in [1]]
SIZES += [10 ** 5 * i for i in [5]]
SIZES += [10 ** 6 * i for i in [3]]
SIZES += [10 ** 7 * i for i in [1, 2, 3, 5, 7, 9]]
SIZES += [10 ** 8 * i for i in [1]]
print(SIZES)


build_times = []
no_index_times = []
index_times = []
insert_times = []
index_sizes = []
for size in SIZES:
    try:
        os.remove('database.db')
    except:
        pass

    conn = sqlite3.connect('database.db')
    print(f"SIZE = {size}")
    c = conn.cursor()
    datafilename = f"./data/csv/osm/osm{size}.csv"

    print("CREATE")
    c.execute('''CREATE TABLE IF NOT EXISTS maps(key INTEGER)''')

    print("IMPORT")
    subprocess.call(["sqlite3", "database.db",
      ".mode csv",
      f".import {datafilename} maps"])

    print("LOAD")
    keys = []
    with open(f'{datafilename}', 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        next(csv_reader, None)
        for i, row in enumerate(csv_reader):
            keys.append(int(row[0]))
            if i == 9:
                break
        print("keys", len(keys))

    print("TIME NO INDEX")
    find_time = 0
    for i, key in enumerate(keys):
        print(f"{i}/{len(keys)}", end="\r")
        start = time.time_ns()
        c.execute(f"SELECT * FROM maps WHERE key = {key}")
        c.fetchone()
        finish = time.time_ns()
        find_time += (finish - start)
    find_time /= len(keys)
    no_index_times.append(find_time)
    print(no_index_times)

    print("BUILD")
    start = time.process_time_ns()
    c.execute('''CREATE INDEX IF NOT EXISTS my_index ON maps(key)''')
    finish = time.process_time_ns()
    build_times.append(finish - start)
    print(build_times)

    print("TIME INDEX")
    print()
    find_time = 0
    for i, key in enumerate(keys):
        print(f"{i}/{len(keys)}", end="\r")
        start = time.time_ns()
        c.execute(f"SELECT * FROM maps WHERE key = {key}")
        c.fetchone()
        finish = time.time_ns()
        find_time += (finish - start)
    find_time /= len(keys)
    index_times.append(find_time)
    print(index_times)

    print("TIME INSERT")
    insert_time = 0
    for i, key in enumerate(keys):
        start = time.process_time_ns()
        c.execute(f'''INSERT INTO maps(key) VALUES ({key})''')
        finish = time.process_time_ns()
        insert_time += (finish - start)
    conn.commit()
    insert_time /= len(keys)
    insert_times.append(insert_time)
    print(insert_times)

    c.execute("SELECT sum(pgsize) FROM dbstat WHERE name = 'my_index'")
    result = c.fetchone()
    index_sizes.append(int(result[0]))
    print(index_sizes)

    c.execute('''DROP INDEX IF EXISTS my_index''')

    c.execute('''DROP TABLE maps''')
    conn.commit()

conn.close()

df = pd.DataFrame()
df["size"] = SIZES
df["build_times"] = build_times
df["no_index_times"] = no_index_times
df["index_times"] = index_times
df["insert_times"] = insert_times
df["index_sizes"] = index_sizes

df.to_csv(CSV_PATH + "sqlite.csv", index=False)
