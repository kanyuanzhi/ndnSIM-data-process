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


if __name__ == "__main__":
    content_amount = 1000
    cache_size = 100
    request_rate = 10.0
    staleness_time = 50
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

    mcav = MCAV(content_amount, cache_size, p_dict, request_rate,
                staleness_time)
    print("node0: ", mcav.totalHitRatio())
    for i in range(3):
        mcav = MCAV(content_amount, cache_size, p_dict, request_rate,
                    staleness_time, mcav.missRate())
        print("node" + str(i + 1), ":", mcav.totalHitRatio())

    print("###############")

    mca = MCA(content_amount, cache_size, p_dict, request_rate)
    print("node0: ", mca.totalHitRatio())
    for i in range(3):
        mca = MCA(content_amount, cache_size, p_dict, request_rate,
                  mca.missRate())
        print("node" + str(i + 1), ":", mca.totalHitRatio())
    # mca0 = MCA(content_amount, cache_size, p_dict, request_rate, staleness_time)
    # mca0_out_rate = mca0.outRate()
    # print mca0.totaHitRatio()

    # mca1 = MCA(content_amount, cache_size, p_dict, request_rate, staleness_time, mca0_out_rate)
    # mca1_out_rate = mca1.outRate()
    # print mca1.totaHitRatio()

    # mca2 = MCA(content_amount, cache_size, p_dict, request_rate, staleness_time, mca1_out_rate)
    # mca2_out_rate = mca2.outRate()
    # print mca2.totaHitRatio()

    # mca3 = MCA(content_amount, cache_size, p_dict, request_rate, staleness_time, mca2_out_rate)
    # mca3_out_rate = mca3.outRate()
    # print mca3.totaHitRatio()

    # mca4 = MCA(content_amount, cache_size, p_dict, request_rate, staleness_time, mca3_out_rate)
    # mca4_out_rate = mca4.outRate()
    # print mca4.totaHitRatio()

    # mca5 = MCA(content_amount, cache_size, p_dict, request_rate, staleness_time, mca4_out_rate)
    # mca5_out_rate = mca5.outRate()
    # print mca5.totaHitRatio()

    # mca6 = MCA(content_amount, cache_size, p_dict, request_rate, staleness_time, mca5_out_rate)
    # mca6_out_rate = mca6.outRate()
    # print mca6.totaHitRatio()

    # mca7 = MCA(content_amount, cache_size, p_dict, request_rate, staleness_time, mca6_out_rate)
    # mca7_out_rate = mca7.outRate()
    # print mca7.totaHitRatio()

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
