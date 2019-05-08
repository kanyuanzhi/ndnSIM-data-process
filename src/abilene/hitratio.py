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
    staleness_time = 60
    z = 0.8  # zipf parameter
    zipf = Zipf(content_amount, z)
    p_dict = zipf.popularity()  # popularity of the contents

    # sca = SCA(content_amount, cache_size, p_dict)
    # ratio = sca.hitRatio()

    # # print sum(ratio.values())

    # sca_validation = SCAValidationEx(
    #     content_amount, cache_size, p_dict, request_rate, staleness_time)
    # ratio_validation = sca_validation.hitRatio()
    # temp1 = 0
    # for i in range(1, content_amount+1):
    #     temp1 = temp1 + ratio[i]*p_dict[i]

    # print "正常的命中率： ", temp1

    # temp2 = 0
    # for i in range(1, content_amount+1):
    #     temp2 = temp2 + ratio_validation[i]*p_dict[i]

    # print "有效性要求的命中率： ", temp2

    # mca = MCA(content_amount, cache_size, p_dict, request_rate, staleness_time)
    # mca_miss_rate = mca.missRate()
    # print "node0: ", mca.totalHitRatio()
    # for i in range(3):
    #     mca = MCA(content_amount, cache_size, p_dict, request_rate, staleness_time, mca_miss_rate)
    #     mca_miss_rate = mca.missRate()
    #     print "node"+str(i+1), mca.totalHitRatio()

    # print "###############"

    # mca = MCANormal(content_amount, cache_size, p_dict, request_rate)
    # mca_miss_rate = mca.missRate()
    # print "node0: ", mca.totalHitRatio()
    # for i in range(3):
    #     mca = MCANormal(content_amount, cache_size, p_dict, request_rate, mca_miss_rate)
    #     mca_miss_rate = mca.missRate()
    #     print "node"+str(i+1), mca.totalHitRatio()
    mca2 = MCAV(content_amount, cache_size, p_dict, request_rate,
               staleness_time)
    mca2_miss_rate = mca2.missRate()
    print("node2: ", mca2.totalHitRatio())

    mca3 = MCAV(content_amount, cache_size, p_dict, request_rate,
               staleness_time)
    mca3_miss_rate = mca3.missRate()
    print("node3: ", mca3.totalHitRatio())

    mca4 = MCAV(content_amount, cache_size, p_dict, request_rate,
               staleness_time)
    mca4_miss_rate = mca4.missRate()
    print("node4: ", mca4.totalHitRatio())

    mca7 = MCAV(content_amount, cache_size, p_dict, request_rate,
               staleness_time)
    mca7_miss_rate = mca7.missRate()
    print("node7: ", mca7.totalHitRatio())

    mca8 = MCAV(content_amount, cache_size, p_dict, request_rate,
               staleness_time)
    mca8_miss_rate = mca8.missRate()
    print("node8: ", mca8.totalHitRatio())

    mca6 = MCAV(content_amount, cache_size, p_dict, request_rate,
               staleness_time, mca7_miss_rate)
    mca6_miss_rate = mca6.missRate()
    print("node6: ", mca6.totalHitRatio())

    mca9 = MCAV(content_amount, cache_size, p_dict, request_rate,
               staleness_time, mca8_miss_rate)
    mca9_miss_rate = mca9.missRate()
    print("node9: ", mca9.totalHitRatio())

    mca23_miss_rate = missMerge(content_amount, mca2_miss_rate, mca3_miss_rate)
    mca1 = MCAV(content_amount, cache_size, p_dict, request_rate,
               staleness_time, mca23_miss_rate)
    mca1_miss_rate = mca1.missRate()
    print("node1: ", mca1.totalHitRatio())

    mca46_miss_rate = missMerge(content_amount, mca4_miss_rate, mca6_miss_rate)
    mca5 = MCAV(content_amount, cache_size, p_dict, request_rate,
               staleness_time, mca46_miss_rate)
    mca5_miss_rate = mca5.missRate()
    print("node5: ", mca5.totalHitRatio())

    mca10 = MCAV(content_amount, cache_size, p_dict, request_rate,
                staleness_time, mca9_miss_rate)
    mca10_miss_rate = mca10.missRate()
    print("node10: ", mca10.totalHitRatio())

    mca1510_miss_rate = missMerge(content_amount, mca1_miss_rate,
                                  mca5_miss_rate, mca10_miss_rate)
    mca0 = MCAV(content_amount, cache_size, p_dict, request_rate,
               staleness_time, mca1510_miss_rate)
    mca0_miss_rate = mca0.missRate()
    print("node0: ", mca0.totalHitRatio())

    ##########

    # single_rate = {}
    # for i in range(1, content_amount + 1):
    #     single_rate[i] = total_rate * p_dict[i]

    # # node1:
    # r_node1 = single_rate   # r_{i,v}
    # p_node1 = {}    # p_{i,v}
    # q_node1 = {}    # q_{i,v}
    # m_node1 = {}    # m_{i,v}

    # for i in range(1, content_amount + 1):
    #     p_node1[i] = r_node1[i] / sum(r_node1.values())
    # sca_node1 = SCA(content_amount, cache_size, p_node1)
    # q_node1 = sca_node1.hitRatio()
    # for i in range(1, content_amount + 1):
    #     m_node1[i] = r_node1[i] * (1 - q_node1[i])

    # # node2:
    # r_node2 = {}
    # p_node2 = {}
    # q_node2 = {}
    # m_node2 = {}

    # for i in range(1, content_amount + 1):
    #     r_node2[i] = single_rate[i] + m_node1[i]
    # for i in range(1, content_amount + 1):
    #     p_node2[i] = r_node2[i] / sum(r_node2.values())
    # sca_node2 = SCA(content_amount, cache_size, p_node2)
    # q_node2 = sca_node2.hitRatio()
    # for i in range(1, content_amount + 1):
    #     m_node2[i] = r_node2[i] * (1 - q_node2[i])

    # # node3:
    # r_node3 = {}
    # p_node3 = {}
    # q_node3 = {}
    # m_node3 = {}

    # for i in range(1, content_amount + 1):
    #     r_node3[i] = single_rate[i] + m_node2[i]
    # for i in range(1, content_amount + 1):
    #     p_node3[i] = r_node3[i] / sum(r_node3.values())
    # sca_node3 = SCA(content_amount, cache_size, p_node3)
    # q_node3 = sca_node3.hitRatio()
    # for i in range(1, content_amount + 1):
    #     m_node3[i] = r_node3[i] * (1 - q_node3[i])

    # print m_node3

    # plt.plot(m_node1.keys(), m_node1.values(),  label='node1')
    # plt.plot(m_node2.keys(), m_node2.values(),  label='node2')
    # plt.plot(m_node3.keys(), m_node3.values(),  label='node3')
    # plt.legend()
    # plt.show()
