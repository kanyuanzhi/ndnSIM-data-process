import math
import matplotlib as mpl
mpl.use('TkAgg')
import matplotlib.pyplot as plt
from mcav.sca import SCA
from mcav.zipf import Zipf
from mcav.scav import SCAV

if __name__ == "__main__":
    content_amount = 1000
    cache_size = 100
    request_rate = 10.0
    staleness_time = 10
    z = 0.8  # zipf parameter
    zipf = Zipf(content_amount, z)
    p_dict = zipf.popularity()  # popularity of the contents

    seq_dict = {}
    name_dict = {}
    f = open("./src/single-node/single-normal.out", "r")
    lines = f.readlines()
    for line in lines:
        # line = line.strip('\n')
        item = line.split(' ')
        if "ndn.ConsumerZipfMandelbrotKan:SendPacket(): [INFO ]" in line:
            index = item.index('for')
            seq = int(item[index+1])
            name = item[len(item)-1]
            if "prefix" in name:
                seq_dict[seq] = name
                name_dict[name] = seq
    #print name_dict

    scav = SCAV(
        content_amount, cache_size, p_dict, request_rate, staleness_time)
    ratio_validation = scav.hitRatio()

    # sca = SCA(content_amount, cache_size, p_dict)
    # ratio_validation = sca.hitRatio()
    print (sum(ratio_validation.values()))
    hitratio_sim = {}
    hitratio_model = {}
    hitcount = {}
    misscount = {}
    index = []
    for line in lines:
        item = line.split(' ')
        if "onContentStoreHit" in line:
            name = item[len(item) - 1].split('=')[1]
            if "prefix" in name:
                seq = name_dict[name]
                if not hitcount.has_key(seq):
                    hitcount[seq] = 1.0
                else:
                    hitcount[seq] = hitcount[seq] + 1
        if "onContentStoreMiss" in line:
            name = item[len(item) - 1].split('=')[1]
            if "prefix" in name:
                seq = name_dict[name]
                if not misscount.has_key(seq):
                    misscount[seq] = 1.0
                else:
                    misscount[seq] = misscount[seq] + 1
    # print hitcount
    for i in range(1, 1001):
        index.append(i)
        if not hitcount.has_key(i):
            hitcount[i] = 0
        if not misscount.has_key(i):
            misscount[i] = 0
        if hitcount[i] + misscount[i] == 0:
             hitratio_sim[i] = 0
        else:
            hitratio_sim[i] = hitcount[i] / (hitcount[i] + misscount[i])
        hitratio_model[i] = ratio_validation[i]

    # for i in range(1, 51):
    #     index.append(i)
    #     name = content_dict[i]
    #     misscount = 0.0
    #     hitcount = 0.0
    #     for line in lines:
    #         if "onContentStoreMiss" in line and name in line:
    #             misscount = misscount + 1
    #         if "onContentStoreHit" in line and name in line:
    #             hitcount = hitcount + 1
    #     hitratio_sim[i] = hitcount / (hitcount + misscount)
    #     hitratio_theory[i] = ratio_validation[i]
    print (p_dict.values()[0:51])
    # print hitcount
    print (hitratio_sim)
    print (hitratio_model)

    plt.plot(index, hitratio_model.values(), label="model")
    plt.plot(index, hitratio_sim.values(), "+", label="simulation")
    plt.xlabel("content ID")
    plt.ylabel("hit ratio")
    plt.grid(True)
    # plt.axis([0, 51, 0, 1])
    plt.legend()
    plt.show()
