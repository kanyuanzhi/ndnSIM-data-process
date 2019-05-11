import matplotlib.pyplot as plt
import sys


def readTXT(txt):
    f = open(txt, "r")
    lines = f.readlines()
    return lines


if __name__ == "__main__":
    lines = readTXT("./src/abilene/abilene120.out")

    nodes = []
    count = 0.0

    for line in lines:
        item = line.split(' ')
        time = item[0]
        if "[DEBUG]" in line and float(time.strip('s')) > 20:
            # if index_str != "-1" and "onContentStoreHit" in line and "/prefix" in line:
            node = item[1]
            if "nfd.Forwarder:onOutgoingInterest():" in line and node == "0":
                count = count + 1
        
    print(round(count/980,5))

    # user_nodes = readTopology("test-tree.txt")
    # user_nodes = [0]

    # lines = readTXT("calculate-data/cs-trace.txt")
    # for i in range(1, len(lines)):
    #     line = lines[i].split("\t")
    #     if int(line[0]) == current_index:
    #         if line[1] in user_nodes:
    #             if line[2] == "CacheHits":
    #                 hits = hits + int(line[3])
    #             if line[2] == "CacheMisses":
    #                 misses = misses + int(line[3])
    #     else:
    #         index_array.append(current_index)
    #         hit_array.append(hits)
    #         miss_array.append(misses)
    #         hit_ratio_array.append(float(hits) / float(hits + misses))
    #         # hits = 0
    #         # misses = 0
    #         current_index = int(line[0])

    # index_array.append(current_index)
    # hit_array.append(hits)
    # miss_array.append(misses)
    # hit_ratio_array.append(float(hits) / float(hits + misses))

    # print index_array
    # print hit_ratio_array

    # plt.plot(index_array, hit_ratio_array)
    # plt.show()
