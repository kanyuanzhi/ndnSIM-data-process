import matplotlib as mpl
mpl.use('TkAgg')
import matplotlib.pyplot as plt

from mcav.zipf import Zipf
from mcav.mcav import MCAV
from mcav.mca import MCA


def saveToTxt(data):
    with open('./src/line/hitratio-staleness-data.txt', 'w') as f:
        for i in range(len(data)):
            f.write(str(data[i]) + '\n')


def missMerge(amount, *misses):
    size = len(misses[0])
    miss_merge = {}
    for i in range(1, amount + 1):
        temp = 0.0
        for j in range(len(misses)):
            temp = temp + misses[j][i]
        miss_merge[i] = temp
    return miss_merge


if __name__ == "__main__":
    content_amount = 1000
    cache_size = 100
    request_rate = 10.0
    staleness_time = 120
    z = 0.8  # zipf parameter
    zipf = Zipf(content_amount, z)
    p_dict = zipf.popularity()  # popularity of the contents
    nodes = 11

    simulation_data = [[] for i in range(nodes)]
    model_data=[[] for i in range(nodes)]

    f = open("./src/abilene/hitratio-staleness-simulation.txt", "r")
    lines = f.readlines()
    i = 0
    for line in lines:
        items = line.split('\t')
        for item in items: 
            simulation_data[i].append(float(item))
        i = i+1

    f = open("./src/abilene/hitratio-staleness-model.txt", "r")
    lines = f.readlines()
    i = 0
    for line in lines:
        items = line.split('\t')
        for item in items: 
            model_data[i].append(float(item))
        i = i+1
    
    index = []
    for time in range(10,121,10):
        index.append(time)

    for node in range(nodes):
        plt.subplot(3, 4, node + 1)
        # plt.title("node "+str(node))
        plt.axis([0, 130, 0, 0.5])
        plt.plot(index, simulation_data[node], '+', label="simulation", color="red")
        plt.plot(index, model_data[node], label="model")
        plt.legend()
        plt.xlabel('node'+str(node)+' staleness time(s)')
        plt.ylabel('hit ratio')
        plt.grid(True)
    plt.show()