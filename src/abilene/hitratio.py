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
    staleness_time = 2000
    z = 0.8  # zipf parameter
    zipf = Zipf(content_amount, z)
    p_dict = zipf.popularity()  # popularity of the contents

    totalHitRatio_dict = {}

    mca2 = MCAV(content_amount, cache_size, p_dict, request_rate,
                staleness_time)
    mca2_miss_rate = mca2.missRate()
    print("node2: ", mca2.totalHitRatio())
    totalHitRatio_dict[2] = mca2.totalHitRatio()

    mca3 = MCAV(content_amount, cache_size, p_dict, request_rate,
                staleness_time)
    mca3_miss_rate = mca3.missRate()
    print("node3: ", mca3.totalHitRatio())
    totalHitRatio_dict[3] = mca3.totalHitRatio()

    mca4 = MCAV(content_amount, cache_size, p_dict, request_rate,
                staleness_time)
    mca4_miss_rate = mca4.missRate()
    print("node4: ", mca4.totalHitRatio())
    totalHitRatio_dict[4] = mca4.totalHitRatio()

    mca7 = MCAV(content_amount, cache_size, p_dict, request_rate,
                staleness_time)
    mca7_miss_rate = mca7.missRate()
    print("node7: ", mca7.totalHitRatio())
    totalHitRatio_dict[7] = mca7.totalHitRatio()

    mca8 = MCAV(content_amount, cache_size, p_dict, request_rate,
                staleness_time)
    mca8_miss_rate = mca8.missRate()
    print("node8: ", mca8.totalHitRatio())
    totalHitRatio_dict[8] = mca8.totalHitRatio()

    mca6 = MCAV(content_amount, cache_size, p_dict, request_rate,
                staleness_time, mca7_miss_rate)
    mca6_miss_rate = mca6.missRate()
    print("node6: ", mca6.totalHitRatio())
    totalHitRatio_dict[6] = mca6.totalHitRatio()

    mca9 = MCAV(content_amount, cache_size, p_dict, request_rate,
                staleness_time, mca8_miss_rate)
    mca9_miss_rate = mca9.missRate()
    print("node9: ", mca9.totalHitRatio())
    totalHitRatio_dict[9] = mca9.totalHitRatio()

    mca23_miss_rate = missMerge(content_amount, mca2_miss_rate, mca3_miss_rate)
    mca1 = MCAV(content_amount, cache_size, p_dict, request_rate,
                staleness_time, mca23_miss_rate)
    mca1_miss_rate = mca1.missRate()
    print("node1: ", mca1.totalHitRatio())
    totalHitRatio_dict[1] = mca1.totalHitRatio()

    mca46_miss_rate = missMerge(content_amount, mca4_miss_rate, mca6_miss_rate)
    mca5 = MCAV(content_amount, cache_size, p_dict, request_rate,
                staleness_time, mca46_miss_rate)
    mca5_miss_rate = mca5.missRate()
    print("node5: ", mca5.totalHitRatio())
    totalHitRatio_dict[5] = mca5.totalHitRatio()

    mca10 = MCAV(content_amount, cache_size, p_dict, request_rate,
                 staleness_time, mca9_miss_rate)
    mca10_miss_rate = mca10.missRate()
    print("node10: ", mca10.totalHitRatio())
    totalHitRatio_dict[10] = mca10.totalHitRatio()

    mca1510_miss_rate = missMerge(content_amount, mca1_miss_rate,
                                  mca5_miss_rate, mca10_miss_rate)
    mca0 = MCAV(content_amount, cache_size, p_dict, request_rate,
                staleness_time, mca1510_miss_rate)
    mca0_miss_rate = mca0.missRate()
    print("node0: ", mca0.totalHitRatio())
    totalHitRatio_dict[0] = mca0.totalHitRatio()

    for i in range(0, 11):
        print(round(totalHitRatio_dict[i],5))
    print(round(sum(list(mca0_miss_rate.values())), 5))

    ##########

    # totalHitRatio_dict = {}

    # mca2 = MCA(content_amount, cache_size, p_dict, request_rate,
    #             )
    # mca2_miss_rate = mca2.missRate()
    # print("node2: ", mca2.totalHitRatio())
    # totalHitRatio_dict[2] = mca2.totalHitRatio()

    # mca3 = MCA(content_amount, cache_size, p_dict, request_rate,
    #             )
    # mca3_miss_rate = mca3.missRate()
    # print("node3: ", mca3.totalHitRatio())
    # totalHitRatio_dict[3] = mca3.totalHitRatio()

    # mca4 = MCA(content_amount, cache_size, p_dict, request_rate,
    #             )
    # mca4_miss_rate = mca4.missRate()
    # print("node4: ", mca4.totalHitRatio())
    # totalHitRatio_dict[4] = mca4.totalHitRatio()

    # mca7 = MCA(content_amount, cache_size, p_dict, request_rate,
    #             )
    # mca7_miss_rate = mca7.missRate()
    # print("node7: ", mca7.totalHitRatio())
    # totalHitRatio_dict[7] = mca7.totalHitRatio()

    # mca8 = MCA(content_amount, cache_size, p_dict, request_rate,
    #             )
    # mca8_miss_rate = mca8.missRate()
    # print("node8: ", mca8.totalHitRatio())
    # totalHitRatio_dict[8] = mca8.totalHitRatio()

    # mca6 = MCA(content_amount, cache_size, p_dict, request_rate,
    #              mca7_miss_rate)
    # mca6_miss_rate = mca6.missRate()
    # print("node6: ", mca6.totalHitRatio())
    # totalHitRatio_dict[6] = mca6.totalHitRatio()

    # mca9 = MCA(content_amount, cache_size, p_dict, request_rate,
    #              mca8_miss_rate)
    # mca9_miss_rate = mca9.missRate()
    # print("node9: ", mca9.totalHitRatio())
    # totalHitRatio_dict[9] = mca9.totalHitRatio()

    # mca23_miss_rate = missMerge(content_amount, mca2_miss_rate, mca3_miss_rate)
    # mca1 = MCA(content_amount, cache_size, p_dict, request_rate,
    #              mca23_miss_rate)
    # mca1_miss_rate = mca1.missRate()
    # print("node1: ", mca1.totalHitRatio())
    # totalHitRatio_dict[1] = mca1.totalHitRatio()

    # mca46_miss_rate = missMerge(content_amount, mca4_miss_rate, mca6_miss_rate)
    # mca5 = MCA(content_amount, cache_size, p_dict, request_rate,
    #              mca46_miss_rate)
    # mca5_miss_rate = mca5.missRate()
    # print("node5: ", mca5.totalHitRatio())
    # totalHitRatio_dict[5] = mca5.totalHitRatio()

    # mca10 = MCA(content_amount, cache_size, p_dict, request_rate,
    #               mca9_miss_rate)
    # mca10_miss_rate = mca10.missRate()
    # print("node10: ", mca10.totalHitRatio())
    # totalHitRatio_dict[10] = mca10.totalHitRatio()

    # mca1510_miss_rate = missMerge(content_amount, mca1_miss_rate,
    #                               mca5_miss_rate, mca10_miss_rate)
    # mca0 = MCA(content_amount, cache_size, p_dict, request_rate, mca1510_miss_rate)
    # mca0_miss_rate = mca0.missRate()
    # print("node0: ", mca0.totalHitRatio())
    # totalHitRatio_dict[0] = mca0.totalHitRatio()

    # for i in range(0, 11):
    #     print(round(totalHitRatio_dict[i],5))

    # print(round(sum(list(mca0_miss_rate.values())), 5))