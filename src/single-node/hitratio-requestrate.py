import math
import matplotlib as mpl
mpl.use('TkAgg')
import matplotlib.pyplot as plt

from mcav.sca import SCA
from mcav.zipf import Zipf
from mcav.scav import SCAV

def saveToTxt(data):
    with open ('./src/single-node/hitratio-requestrate-data.txt','w') as f:
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
    f = open("./src/single-node/hitratio-requestrate.txt", "r")
    lines = f.readlines()
    for line in lines:
        item = line.split('\t')
        index_txt.append(int(item[0]))
        data_txt.append(float(item[1]))

    index = []
    data_validation = []
    for i in range(5, 55, 5):
        print(i)
        index.append(i)
        scav = SCAV(
            content_amount, cache_size, p_dict, float(i), staleness_time)
        data_validation.append(scav.totalHitRatio())
    print(data_validation)
    #data_validation=[0.20261753226812357, 0.2689436282156983, 0.29814070628461814, 0.3150620402701798, 0.32623924159054435, 0.33422440401500125, 0.3402370008044255, 0.34493845488027663, 0.3487206595809369, 0.3518315410218549]
    saveToTxt(data_validation)
    plt.plot(index, data_validation, label='theory-validation')
    plt.plot(index_txt, data_txt, '*', label='simulation-validation')
    plt.legend()
    plt.axis([0,60,0,1])
    plt.show()
