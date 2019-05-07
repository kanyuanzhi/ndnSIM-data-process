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


class SCAValidationExTest(object):
    # realize the SCA algorithm
    def __init__(self, amount, size, popurity_dict, rate, time):
        self._amount = amount
        self._size = size
        self._alpha = popurity_dict
        self._P = {}
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
            # if i == self._size:
            #     self._computePB(i)
        return self._B[self._size]

    def _computeP(self, position):
        # position starts from 2
        p = {}
        molecule1 = 0.0
        molecule2 = 0.0
        denominator1 = 0.0
        denominator2 = 0.0
        for i in range(1, self._amount + 1):
            denominator1 = denominator1 + \
                self._nonNegative(
                    self._alpha[i] * (1 - self._B[position-1][i]))
        for i in range(1, self._amount + 1):
            molecule1 = self._nonNegative(
                self._alpha[i] * (1 - self._B[position-1][i]))*self._validation_probability[i]
            #p[i] = molecule1 / denominator1 + molecule2 / denominator2
            p[i] = molecule1 / denominator1
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
            vp[i] = 1 - math.pow(math.e, -self._alpha[i] * self._validation_rate*self._staleness_time)
        # print vp
        return vp

    def _validationRate(self):
        validation_rate =  self._request_rate * math.pow(math.e, - self._size / self._staleness_time/self._request_rate)
        return validation_rate
    # def _validationRate(self):
    #     validation_rate = {}
    #     for i in range(1, self._amount+1):
    #         validation_rate[i] = self._alpha[i] *self._request_rate
    #     return validation_rate

    def _computeP1(self):
        P1 = {}
        for i in range(1, self._amount + 1):
            P1[i] = self._alpha[i] * self._validation_probability[i]
        return P1


def delta(a1, a2):
    total = 0.0
    for i in range(21):
        total = total + math.fabs(a1[i]-a2[i])/a2[i]
    return total/20


if __name__ == "__main__":
    content_amount = 1000
    cache_size = 100
    request_rate = 10.0
    staleness_time = 40
    z = 0.8  # zipf parameter
    zipf = Zipf(content_amount, z)
    p_dict = zipf.popularity()  # popularity of the contents

    seq_dict = {}
    name_dict = {}
    f = open("./src/single-node/single40.out", "r")
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

    sca_validation = SCAValidationExTest(
        content_amount, cache_size, p_dict, request_rate, staleness_time)
    ratio_validation = sca_validation.hitRatio()

    sca = SCA(content_amount, cache_size, p_dict)
    ratio = sca.hitRatio()
    #print sum(ratio_validation.values())
    hitratio_sim = {}
    hitratio_model = {}
    hitratio_validation_model = {}
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
        hitratio_model[i] = ratio[i]
        hitratio_validation_model[i] = ratio_validation[i]

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
    # print p_dict.values()
    # print hitratio_sim
    # print hitratio_model

    # print delta(hitratio_validation_model.values(),hitratio_sim.values())
    temp_validation = 0
    # temp = 0
    for j in range(1, content_amount+1):
        temp_validation = temp_validation + ratio_validation[j]*p_dict[j]
        # temp = temp + ratio[j]*p_dict[j]
    print temp_validation

    plt.plot(index, hitratio_model.values(), label="model")
    plt.plot(index, hitratio_validation_model.values(),
             label="validation-model")
    plt.plot(index, hitratio_sim.values(), "+", label="simulation")
    plt.xlabel("content ID")
    plt.ylabel("hit ratio")
    plt.grid(True)
    # plt.axis([0, 51, 0, 1])
    plt.legend()
    plt.show()
