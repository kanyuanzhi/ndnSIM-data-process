import matplotlib as mpl
mpl.use('TkAgg')
import matplotlib.pyplot as plt

from mcav.zipf import Zipf
from mcav.mcav import MCAV
from mcav.mca import MCA


def saveToTxt(hit_ratio):
    size = len(hit_ratio[0])
    # keys = list(hit_ratio[0].keys())
    # keys.sort()
    with open('./src/line/hitratio-line-data.txt', 'w') as f:
        for i in range(size):
            line = ""
            for j in range(len(hit_ratio)):
                line = line + str(hit_ratio[j][i]) + '\t'
            line = line + '\n'
            f.write(line)


if __name__ == "__main__":
    content_amount = 1000
    cache_size = 100
    request_rate = 10.0
    staleness_time = 50
    z = 0.8  # zipf parameter
    zipf = Zipf(content_amount, z)
    p_dict = zipf.popularity()  # popularity of the contents
    nodes = 4

    hit_ratio_txt = {0: [], 1: [], 2: [], 3: []}
    index_txt = []
    f = open("./src/line/hitratio-staleness.txt", "r")
    lines = f.readlines()
    for line in lines:
        item = line.split('\t')
        index_txt.append(int(item[0]))
        for i in range(nodes):
            hit_ratio_txt[i].append(float(item[i + 1]))

    hit_ratio = {0: [], 1: [], 2: [], 3: []}
    f = open("./src/line/hitratio-line-data.txt", "r")
    lines = f.readlines()
    for line in lines:
        item = line.split('\t')
        for i in range(nodes):
            hit_ratio[i].append(float(item[i]))

    # hit_ratio_0 = []
    # hit_ratio_1 = []
    # hit_ratio_2 = []
    # hit_ratio_3 = []

    # hit_ratio = {
    #     0: hit_ratio_0,
    #     1: hit_ratio_1,
    #     2: hit_ratio_2,
    #     3: hit_ratio_3
    # }

    index = []
    for i in range(10, 125, 5):
        print(i)
        index.append(i)
    #     mcav = MCAV(content_amount, cache_size, p_dict, request_rate, i)
    #     hit_ratio[0].append(mcav.totalHitRatio())
    #     for j in range(1, nodes):
    #         mcav = MCAV(content_amount, cache_size, p_dict, request_rate, i,
    #                     mcav.missRate())
    #         hit_ratio[j].append(mcav.totalHitRatio())
    # print(hit_ratio)
    # saveToTxt(hit_ratio)
    for i in range(nodes):
        plt.subplot(2, 2, i + 1)
        plt.axis([0, 130, 0, 0.5])
        plt.plot(index, hit_ratio[i], label="node" + str(i) + "-model")
        plt.plot(index_txt,
                 hit_ratio_txt[i],
                 '+',
                 label="node" + str(i) + "-simulation",
                 color="red")
        plt.legend()
        plt.xlabel('staleness time(s)')
        plt.ylabel('hit ratio')
        plt.grid(True)
    plt.show()
