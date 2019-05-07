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
    lines = readTXT("calculate-data/cs-trace.txt")
    nodes = []
    hit_count = {}
    miss_count = {}

    for i in range(1, len(lines)):
        
        line = lines[i].split("\t")
        time = int(line[0])
        node = int(line[1])
        flag = line[2]
        count = float(line[3])
        if time > 10:
            if node in nodes:
                if flag == "CacheHits":
                    hit_count[node] = hit_count[node] + count
                if flag == "CacheMisses":
                    miss_count[node] = miss_count[node] + count
            else:
                nodes.append(node)
                if flag == "CacheHits":
                    hit_count[node] = count
                    miss_count[node] = 0.0
                if flag == "CacheMisses":
                    hit_count[node] = 0.0
                    miss_count[node] = count
    nodes.sort()
    for node in nodes:
        print "node",node,": ",hit_count[node]/(hit_count[node]+miss_count[node])
    
    # print hits, misses, float(hits)/float(hits+misses)

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
