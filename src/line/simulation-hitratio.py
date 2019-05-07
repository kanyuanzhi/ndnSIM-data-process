import matplotlib.pyplot as plt
import sys


def readTXT(txt):
    f = open(txt, "r")
    lines = f.readlines()
    return lines



if __name__ == "__main__":
    lines = readTXT("./src/line/120.out")

    nodes = []
    hit_ratio = {}
    hit_count = {}
    miss_count ={}

    for line in lines:
        item = line.split(' ')
        time = item[0]
        if "[DEBUG]" in line and float(time.strip('s')) > 20:
        # if index_str != "-1" and "onContentStoreHit" in line and "/prefix" in line:
            if "STATICFLAG" in line and "hit_count" in line:
                index = int(item[item.index("hit_count")+1])
                if index not in nodes:
                    nodes.append(index)
                    hit_count[index] = 1.0
                    miss_count[index] = 0.0
                else:
                    hit_count[index] = hit_count[index] + 1
            # if index_str != "-1" and "onContentStoreMiss" in line and "/prefix" in line:
            #     index = int(index_str)
            if "STATICFLAG" in line and "miss_count" in line:
                index = int(item[item.index("miss_count")+1])
                if index not in nodes:
                    nodes.append(index)
                    hit_count[index] = 0.0
                    miss_count[index] = 1.0
                else:
                    miss_count[index] = miss_count[index] + 1
    print nodes
    for i in range(len(nodes)):
        hit_ratio[i] = hit_count[i] / (hit_count[i] + miss_count[i])
    
    print hit_ratio




    

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
