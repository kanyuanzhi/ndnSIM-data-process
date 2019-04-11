import matplotlib.pyplot as plt
import sys


def readTXT(txt):
    f = open(txt, "r")
    lines = f.readlines()
    return lines


def readTopology(txt):
    lines = readTXT(txt)
    user_nodes = []
    for line in lines:
        item = line.split(" ")[0]
        if "user" in item:
            user_nodes.append(item)
        if "link" in item:
            return user_nodes


if __name__ == "__main__":
    index_array = []
    hit_array = []
    miss_array = []
    hit_ratio_array = []
    hits = 0
    misses = 0
    current_index = 1

    user_nodes = readTopology("test-tree.txt")

    lines = readTXT("cs/cs-trace.txt")
    for i in range(1, len(lines)):
        line = lines[i].split("\t")
        if int(line[0]) == current_index:
            if line[1] in user_nodes:
                if line[2] == "CacheHits":
                    hits = hits + int(line[3])
                if line[2] == "CacheMisses":
                    misses = misses + int(line[3])
        else:
            index_array.append(current_index)
            hit_array.append(hits)
            miss_array.append(misses)
            hit_ratio_array.append(float(hits) / float(hits + misses))
            # hits = 0
            # misses = 0
            current_index = int(line[0])

    index_array.append(current_index)
    hit_array.append(hits)
    miss_array.append(misses)
    hit_ratio_array.append(float(hits) / float(hits + misses))

    print index_array
    print hit_ratio_array

    plt.plot(index_array, hit_ratio_array)
    plt.show()
