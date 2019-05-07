import math
import matplotlib.pyplot as plt


class Zipf(object):
    # calucate the popularity of the contents
    def __init__(self, amount, z):
        self._amount = amount
        self._z = z
        self._factor = self._normalization()

    def _normalization(self):
        factor = 0.0
        for i in range(1, self._amount + 1):
            factor = factor + math.pow(1.0/i, self._z)
        return 1/factor

    def popularity(self):
        popularity_dict = {}
        for i in range(1, self._amount + 1):
            # popularity_dict[self._amount + 1 - i] = self._factor/math.pow(i, self._z)
            popularity_dict[i] = self._factor/math.pow(i, self._z)
        return popularity_dict


class SCA(object):
    # realize the SCA algorithm
    def __init__(self, amount, size, popurity_dict):
        self._amount = amount
        self._size = size
        self._alpha = popurity_dict
        self._P = {}
        self._P[1] = self._alpha
        self._B = {}

    def hitRatio(self):
        for i in range(1, self._size + 1):
            self._computeB(i)
            i = i + 1
            if i <= self._size:
                self._computeP(i)
        return self._B[self._size]

    def _computeP(self, position):
        # position starts from 2
        p = {}
        molecule = []
        denominator = 0.0
        for i in range(1, self._amount + 1):
            denominator = denominator + \
                self._nonNegative(
                    self._alpha[i] * (1 - self._B[position-1][i]))
        for i in range(1, self._amount + 1):
            molecule.append(self._nonNegative(
                self._alpha[i] * (1 - self._B[position-1][i])))
            p[i] = molecule[i-1] / denominator
        self._P[position] = p
        # print p
        # print sum(p.values())
        # print "-----=------"

    def _computeB(self, position):
        # position starts from 1
        b = {}
        for i in range(1, self._amount + 1):
            b[i] = 0.0
            for j in range(1, position + 1):
                b[i] = b[i] + self._P[j][i]
        self._B[position] = b

    def _nonNegative(self, number):
        if number > 0:
            return number
        else:
            return 0.0


class SCAValidationEx(object):
    # realize the SCA algorithm
    def __init__(self, amount, size, popularity_dict, rate, time):
        self._amount = amount
        self._size = size
        self._alpha = popularity_dict
        self._P = {}
        # self._P[1] = self._alpha
        self._B = {}
        self._request_rate = rate
        self._staleness_time = time
        self._validation_rate = self._validationRate()
        self._validation_probability = self._validationProbability()
        self._P[1] = self._computeP1()

    def hitRatio(self):
        for i in range(1, self._size + 1):
            self._computeB(i)
            i = i + 1
            if i <= self._size:
                self._computeP(i)
        return self._B[self._size]

    def _computeP(self, position):
        # position starts from 2
        p = {}
        molecule = []
        denominator = 0.0
        for i in range(1, self._amount + 1):
            denominator = denominator + \
                self._nonNegative(
                    self._alpha[i] * (1 - self._B[position-1][i]))
        for i in range(1, self._amount + 1):
            molecule.append(self._nonNegative(
                self._alpha[i] * (1 - self._B[position-1][i])))
            p[i] = self._validation_probability[i] * molecule[i-1] / denominator
        self._P[position] = p
        # print p
        # print sum(p.values())
        # print "-----=------"

    def _computeB(self, position):
        # position starts from 1
        b = {}
        for i in range(1, self._amount + 1):
            b[i] = 0.0
            for j in range(1, position + 1):
                b[i] = b[i] + self._P[j][i]
        self._B[position] = b

    def _nonNegative(self, number):
        if number > 0:
            return number
        else:
            return 0.0

    def _validationProbability(self):
        vp = {}
        for i in range(1, self._amount + 1):
            vp[i] = 1 - math.pow(math.e, - self._alpha[i]
                                 * self._validation_rate * self._staleness_time)
        # print vp
        return vp

    # def _validationRate(self):
    #     validation_rate = self._request_rate * \
    #         (1 - math.pow(math.e, - self._request_rate*self._staleness_time / self._size))
    #     return validation_rate
    
    def _validationRate(self):
        validation_rate = self._request_rate *  math.pow(math.e, - self._size/self._staleness_time/self._request_rate )
        return validation_rate

    # def _validationRate(self):
    #     validation_rate = self._request_rate * self._staleness_time*self._request_rate/self._size *  math.pow(math.e, - self._size/self._staleness_time/self._request_rate )
    #     return validation_rate

    def _computeP1(self):
        P1 = {}
        for i in range(1, self._amount + 1):
            P1[i] = self._alpha[i] * self._validation_probability[i]
        return P1
        
def saveToTxt(data):
    with open ('./src/line/hitratio-staleness-data.txt','w') as f:
        for i in range(len(data)):
            f.write(str(data[i])+'\n')


class MCA(object):
    # realize the MCA algorithm
    def __init__(self, amount, size, popularity_dict, rate, time, miss_rate={}):
        self._amount = amount
        self._size = size
        self._popularity = popularity_dict
        self._staleness_time = time
        self._rate = rate   # a number
        self._miss_rate = miss_rate # a dict

        self._total_rate = self._totalRate()
        self._request_probability = self._requestProbability()
        self._sca_validation = SCAValidationEx(amount, size, self._request_probability, sum(self._total_rate.values()), time)
        self._sca = SCA(amount, size, self._request_probability)
        self._hit_ratio = self._sca_validation.hitRatio()
        self._hit_ratio_sca = self._sca.hitRatio()

    def hitRatio(self):
        return self._hit_ratio

    def totaHitRatio(self):
        h = 0
        for i in range(1, self._amount + 1):
            h = h + self._request_probability[i] * self._hit_ratio[i]
        return h

    def outRate(self):
        m = {}
        for i in range(1, self._amount + 1):
            m[i] = self._total_rate[i] * (1 - self._hit_ratio[i])
        return m

    def _totalRate(self):
        r = {}
        if self._miss_rate:
            for i in range(1, self._amount + 1):
                r[i] = self._rate * self._popularity[i] + self._miss_rate[i]
        else:
            for i in range(1, self._amount + 1):
                r[i] = self._rate * self._popularity[i]
        return r

    def _requestProbability(self):
        p = {}
        for i in range(1, self._amount + 1):
            p[i] = self._total_rate[i] / sum(self._total_rate.values())
        return p

class MCANormal(object):
    # realize the MCA algorithm
    def __init__(self, amount, size, popularity_dict, rate, miss_rate={}):
        self._amount = amount
        self._size = size
        self._popularity = popularity_dict
        self._rate = rate   # a number
        self._miss_rate = miss_rate # a dict

        self._total_rate = self._totalRate()
        self._request_probability = self._requestProbability()
        self._sca = SCA(amount, size, self._request_probability)
        self._hit_ratio = self._sca.hitRatio()

    def hitRatio(self):
        return self._hit_ratio

    def totaHitRatio(self):
        h = 0
        for i in range(1, self._amount + 1):
            h = h + self._request_probability[i] * self._hit_ratio[i]
        return h

    def outRate(self):
        m = {}
        for i in range(1, self._amount + 1):
            m[i] = self._total_rate[i] * (1 - self._hit_ratio[i])
        return m

    def _totalRate(self):
        r = {}
        if self._miss_rate:
            for i in range(1, self._amount + 1):
                r[i] = self._rate * self._popularity[i] + self._miss_rate[i]
        else:
            for i in range(1, self._amount + 1):
                r[i] = self._rate * self._popularity[i]
        return r

    def _requestProbability(self):
        p = {}
        for i in range(1, self._amount + 1):
            p[i] = self._total_rate[i] / sum(self._total_rate.values())
        return p

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

    mca = MCA(content_amount, cache_size, p_dict, request_rate, staleness_time)
    mca_out_rate = mca.outRate()
    print "node0: ", mca.totaHitRatio()
    for i in range(3):
        mca = MCA(content_amount, cache_size, p_dict, request_rate, staleness_time, mca_out_rate)
        mca_out_rate = mca.outRate()
        print "node"+str(i+1), mca.totaHitRatio()

    print "###############"
    
    mca = MCANormal(content_amount, cache_size, p_dict, request_rate)
    mca_out_rate = mca.outRate()
    print "node0: ", mca.totaHitRatio()
    for i in range(3):
        mca = MCANormal(content_amount, cache_size, p_dict, request_rate, mca_out_rate)
        mca_out_rate = mca.outRate()
        print "node"+str(i+1), mca.totaHitRatio()
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
