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
    def __init__(self, amount, size, popurity_dict, rate, time):
        self._amount = amount
        self._size = size
        self._alpha = popurity_dict
        self._P = {}
        # self._P[1] = self._alpha
        self._B = {}
        self._validation_rate = rate
        self._staleness_time = time
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
            vp[i] = 1 - math.pow(math.e, - self._alpha[i] * self._validation_rate*(1 - math.pow(math.e, -1.5*self._staleness_time))*self._staleness_time)
        # print vp
        return vp

    def _computeP1(self):
        P1 = {}
        for i in range(1, self._amount + 1):
            P1[i] = self._alpha[i] * self._validation_probability[i]
        return P1


if __name__ == "__main__":
    content_amount = 1000
    cache_size = 80
    total_rate = 10.0
    validation_rate = 10.0
    staleness_time = 20
    z = 0.8  # zipf parameter
    zipf = Zipf(content_amount, z)
    p_dict = zipf.popularity()  # popularity of the contents
    #print p_dict

    # sca_validation = SCAValidationEx(
    #     content_amount, cache_size, p_dict, validation_rate, staleness_time)
    # ratio_validation = sca_validation.hitRatio()
    # temp_validation = 0
    # for j in range(1, content_amount+1):
    #     temp_validation = temp_validation + ratio_validation[j]*p_dict[j]
    # print temp_validation

    index_txt = []
    data_txt = []
    f = open("./src/single/hitratio-cachesize.txt", "r")
    lines = f.readlines()
    for line in lines:
        item = line.split('\t')
        index_txt.append(int(item[0]))
        data_txt.append(float(item[1]))

    index = []
    data = []
    data_validation = []
    # sca = SCA(content_amount, cache_size, p_dict)
    # ratio = sca.hitRatio()
    # temp = 0
    # for j in range(1, content_amount+1):
    #     temp = temp + ratio[j]*p_dict[j]
    # data = [temp for i in range(10)]
    for i in range(20, 220, 20):
        print i
        index.append(i)
        sca_validation = SCAValidationEx(
            content_amount, i, p_dict, validation_rate, 20)
        ratio_validation = sca_validation.hitRatio()
        sca = SCA(content_amount, i, p_dict)
        ratio = sca.hitRatio()
        temp_validation = 0
        temp = 0
        for j in range(1, content_amount+1):
            temp = temp + ratio[j]*p_dict[j]
            temp_validation = temp_validation + ratio_validation[j]*p_dict[j]

        
        data.append(temp)
        data_validation.append(temp_validation)
    print(data_validation)
    #data_validation=[0.16809811407636926, 0.23302533300322498, 0.26678899724721633, 0.2874161596588254, 0.3012545456597677, 0.31118737474259456, 0.31869722658862937, 0.32461109991795933, 0.3294198022690047, 0.3334298803654445, 0.3368414414603373, 0.33979034612238307, 0.342372155590429, 0.34465625636867325, 0.3466944767762228, 0.3485265073329162, 0.3501834101745586, 0.3516899543881345]
    plt.plot(index, data, label='theory-normal')
    plt.plot(index, data_validation, label='theory-validation')
    plt.plot(index_txt, data_txt, '*', label='simulation-validation')
    plt.legend()
    plt.show()

    # index = []
    # data_validation = []
    # for i in range(5, 100, 5):
    #     sca_validation = SCAValidationEx(
    #         content_amount, 20, p_dict, validation_rate, i)
    #     ratio_validation = sca_validation.hitRatio()
    #     temp_validation = 0.0
    #     for j in range(1, content_amount+1):
    #         temp_validation = temp_validation + ratio_validation[j]*p_dict[j]
    #     data_validation.append(temp_validation)
    #     index.append(i)
    # plt.plot(index, data_validation, '-o', label='validation')
    # plt.legend()
    # plt.show()
    # temp = 0
    # for i in range(1, content_amount+1):
    #     temp = temp + ratio[i]*p_dict[i]
