from time import process_time_ns

from utils.distributions import uniform_keys, positions, graph

from lindex.lindex import Lindex

if __name__ == "__main__":
    print("CREATE")
    index = Lindex(uniform_keys, positions)
    print("TRAIN")
    start = process_time_ns()
    index.train()
    print(f"Train Time: {(process_time_ns() - start) / 10 ** 9}")
    print("PREDICT")
    spos = []
    npos = []
    for i, key in enumerate(uniform_keys):
        if i % 100 == 0:
            print(f"{i}/{len(uniform_keys)}: key = {key}")
        pos_s, pos_n = index.predict(key)
        spos.append(pos_s)
        npos.append(pos_n)
    print("STOP")

    graph(uniform_keys, positions, [spos, npos], ["sort", "non_sort"])

