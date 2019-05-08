import math
import matplotlib as mpl
mpl.use('TkAgg')
import matplotlib.pyplot as plt

from mcav.sca import SCA
from mcav.zipf import Zipf
from mcav.scav import SCAV

def saveToTxt(data):
    with open ('./src/single-node/hitratio-cachesize-data.txt','w') as f:
        for i in range(len(data)):
            f.write(str(data[i])+'\n')


if __name__ == "__main__":
    content_amount = 1000
    cache_size = 80
    request_rate = 10.0
    staleness_time = 20
    z = 0.8  # zipf parameter
    zipf = Zipf(content_amount, z)
    p_dict = zipf.popularity()  # popularity of the contents

    index_txt = []
    data_txt = []
    f = open("./src/single-node/hitratio-cachesize.txt", "r")
    lines = f.readlines()
    for line in lines:
        item = line.split('\t')
        index_txt.append(int(item[0]))
        data_txt.append(float(item[1]))

    index = []
    data = []
    data_validation = []
    for i in range(20, 201, 10):
        print (i)
        index.append(i)
        scav = SCAV(
            content_amount, i, p_dict, request_rate, staleness_time)
        sca = SCA(content_amount, i, p_dict)
        data.append(sca.totalHitRatio())
        data_validation.append(scav.totalHitRatio())
    print (data)
    print (data_validation)
    # data = [0.1441581832221518, 0.19173576710899384, 0.23013971045760404, 0.2624409495888261, 0.2905165678636614, 0.31551722374378127, 0.3381718801806883, 0.35896566626072873, 0.37823863826484116, 0.3962402303902439, 0.41316008303220864, 0.42914638086485024, 0.44431741051235857, 0.45876924223655224, 0.47258105439351505, 0.4858189402788215, 0.4985386939356977, 0.510787887211904, 0.5226074436521276]
    # data_validation = [0.12516568278035548, 0.1610245641188828, 0.1894984094137348, 0.2088483479120813, 0.2271988968586757, 0.2385382293709827, 0.25183842560249237, 0.2585945046107257, 0.2689436282156983, 0.27273966765279334, 0.28116621534844516, 0.282902062215111, 0.2899831717167317, 0.2902118472109087, 0.29630175674658643, 0.29538691803242373, 0.30071725648010983, 0.2989104314310563, 0.30364031782847556]
    print (data_validation[10])
    saveToTxt(data_validation)
    #data_validation=[0.16809811407636926, 0.23302533300322498, 0.26678899724721633, 0.2874161596588254, 0.3012545456597677, 0.31118737474259456, 0.31869722658862937, 0.32461109991795933, 0.3294198022690047, 0.3334298803654445, 0.3368414414603373, 0.33979034612238307, 0.342372155590429, 0.34465625636867325, 0.3466944767762228, 0.3485265073329162, 0.3501834101745586, 0.3516899543881345]
    plt.plot(index, data, label='model-SCA')
    plt.plot(index, data_validation, label='model-SCAV')
    plt.plot(index_txt, data_txt, '+', label='simulation', color="red")
    plt.xlabel("cache size")
    plt.ylabel("hit ratio")
    plt.grid(True)
    plt.axis([10,210,0,1])
    plt.legend()
    plt.show()
