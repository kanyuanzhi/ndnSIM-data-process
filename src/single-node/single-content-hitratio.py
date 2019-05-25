from math import pow, e
import matplotlib as mpl
mpl.use('TkAgg')
import matplotlib.pyplot as plt
from mcav.sca import SCA
from mcav.zipf import Zipf
# from mcav.scav import SCAV
class SCAV(object):
    # realize the SCA algorithm
    def __init__(self, amount, size, popularity, rate, time):
        self._amount = amount
        self._size = size
        self._alpha = popularity
        self._P = {}
        # self._P[1] = self._alpha
        self._B = {}
        self._request_rate = rate
        self._staleness_time = time
        self._validation_rate = self._validationRate()
        self._validation_probability = self._validationProbability()
        self._P[1] = self._computeP1()
        self._hitRatio()

    def hitRatio(self):
        return self._B[self._size]

    def totalHitRatio(self):
        total_hit_ratio = 0.0
        for i in range(1, self._amount + 1):
            total_hit_ratio = total_hit_ratio + \
                self._alpha[i]*self._B[self._size][i]
        return total_hit_ratio

    def _hitRatio(self):
        for i in range(1, self._size + 1):
            self._computeB(i)
            i = i + 1
            if i <= self._size:
                self._computeP(i)

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
            molecule = self._nonNegative(self._alpha[i] *
                                         (1 - self._B[position - 1][i]))
            p[i] = self._validation_probability[i][position] * molecule / denominator

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
        VP = {}
        for i in range(1, self._amount + 1):
            vp = {}
            for j in range(1, self._size + 1):
                vp[j] = 1 - pow(
                    e, -self._validation_rate[i] * self._staleness_time *
                    (1 - pow(e, -(j - 1))))
                # vp[j] = 1-pow(e,-self._validation_rate[i]*self._staleness_time*j/self._size)
            VP[i] = vp
        return VP

    def _validationRate(self):
        validation_rate = {}
        for i in range(1, self._amount + 1):
            i_request_rate = self._alpha[i] * self._request_rate
            validation_rate[i] = i_request_rate
        return validation_rate

    def _computeP1(self):
        P1 = {}
        for i in range(1, self._amount + 1):
            P1[i] = self._alpha[i] * self._validation_probability[i][1]
        return P1



if __name__ == "__main__":
    content_amount = 10000
    cache_size = 100
    request_rate = 10.0
    staleness_time = 5
    z = 0.8  # zipf parameter
    zipf = Zipf(content_amount, z) 
    p_dict = zipf.popularity()  # popularity of the contents

    seq_dict = {}
    name_dict = {}
    f = open("./src/single-node/out.log", "r")
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

    # scav = SCAV(
    #     content_amount, cache_size, p_dict, request_rate, staleness_time)
    # ratio_validation = scav.hitRatio()

    sca = SCA(content_amount, cache_size, p_dict)
    ratio_validation = sca.hitRatio()
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
                if not seq in hitcount:
                    hitcount[seq] = 1.0
                else:
                    hitcount[seq] = hitcount[seq] + 1
        if "onContentStoreMiss" in line:
            name = item[len(item) - 1].split('=')[1]
            if "prefix" in name:
                seq = name_dict[name]
                if not seq in misscount:
                    misscount[seq] = 1.0
                else:
                    misscount[seq] = misscount[seq] + 1
    # print hitcount
    for i in range(1, 51):
        index.append(i)
        if not i in hitcount:
            hitcount[i] = 0
        if not i in misscount:
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
    # print hitcount
    print (hitratio_sim)
    print (hitratio_model)

    plt.plot(index, list(hitratio_model.values()), label="model")
    plt.plot(index, list(hitratio_sim.values()), "+", label="simulation")
    plt.xlabel("content ID")
    plt.ylabel("hit ratio")
    plt.grid(True)
    # plt.axis([0, 51, 0, 1])
    plt.legend()
    plt.show()
