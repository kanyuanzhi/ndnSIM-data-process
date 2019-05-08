import matplotlib as mpl
mpl.use('TkAgg')
import matplotlib.pyplot as plt

from mcav.sca import SCA
from mcav.zipf import Zipf
from mcav.scav import SCAV

def saveToTxt(data):
    with open ('./src/single-node/hitratio-staleness-data.txt','w') as f:
        for i in range(len(data)):
            f.write(str(data[i])+'\n')

if __name__ == "__main__":
    content_amount = 1000
    cache_size = 100
    request_rate = 10.0
    staleness_time = 20
    z = 0.8  # zipf parameter
    zipf = Zipf(content_amount, z)
    p_dict = zipf.popularity()  # popularity of the contents

    index_txt = []
    data_txt = []
    f = open("./src/single-node/hitratio-staleness.txt", "r")
    lines = f.readlines()
    for line in lines:
        item = line.split('\t')
        index_txt.append(int(item[0]))
        data_txt.append(float(item[1]))

    index = []
    data = []
    data_validation = []
    sca = SCA(content_amount, cache_size, p_dict)
    total_ratio = sca.totalHitRatio()

    for i in range(5, 121, 5):
        print (i)
        index.append(i)
        data.append(total_ratio)
        sca_validation = SCAV(
            content_amount, cache_size, p_dict, request_rate, i)
        data_validation.append(sca_validation.totalHitRatio())
    print(data_validation)
    # data_validation = [0.112428673342427, 0.20261753226812357, 0.2422101866416663, 0.2689436282156983, 0.28582385256037496, 0.2949111857517776, 0.30692548131609065, 0.31289325064290957, 0.31794290609920933, 0.32623924159054435, 0.3298618880057964, 0.33303990158448593, 0.3358533459249052, 0.33836362156566246, 0.34061870748426637, 0.34265670541834925, 0.3445083022503371, 0.34619852114569727, 0.34774799253942457, 0.3518315410218549, 0.35307016934848706, 0.3542161281411062, 0.355279477605182, 0.3562688449867552]
    saveToTxt(data_validation)
    plt.plot(index, data, label='model-SCA')
    plt.plot(index, data_validation, label='model-SCAV')
    plt.plot(index_txt, data_txt, '+', label='simulation', color="red")
    plt.xlabel("staleness time(s)")
    plt.ylabel("hit ratio")
    plt.axis([0,125,0,0.5])
    plt.grid(True)
    plt.legend()
    plt.show()
