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
    ppos = []
    for i, key in enumerate(uniform_keys):
        if i % 100 == 0:
            print(f"{i}/{len(uniform_keys)}: key = {key}")
        pos = index.predict(key)
        ppos.append(pos)
    print("STOP")

    graph(uniform_keys, positions, [ppos])

