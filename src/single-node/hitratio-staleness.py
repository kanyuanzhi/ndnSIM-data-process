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
    def __init__(self, amount, size, popularity_dict):
        self._amount = amount
        self._size = size
        self._alpha = popularity_dict
        self._P = {}
        self._P[1] = self._alpha
        self._B = {}
        self._hitRatio()

    def hitRatio(self):
        return self._B[self._size]

    def totalHitRatio(self):
        total_hit_ratio = 0.0
        for i in range(1, self._amount+1):
            total_hit_ratio = total_hit_ratio + self._alpha[i]*self._B[self._size][i]
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
        for i in range(1, self._amount+1):
            total_hit_ratio = total_hit_ratio + self._alpha[i]*self._B[self._size][i]
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
    
    def _validationRate(self):
        validation_rate = self._request_rate *  math.pow(math.e, - self._size/self._staleness_time/self._request_rate )
        return validation_rate


    def _computeP1(self):
        P1 = {}
        for i in range(1, self._amount + 1):
            P1[i] = self._alpha[i] * self._validation_probability[i]
        return P1
        
def saveToTxt(data):
    with open ('./src/single-node/hitratio-staleness-data.txt','w') as f:
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
    f = open("./src/single-node/hitratio-staleness.txt", "r")
    lines = f.readlines()
    for line in lines:
        item = line.split('\t')
        index_txt.append(int(item[0]))
        data_txt.append(float(item[1]))

    index = []
    data = []
    data_validation = []
    sca = SCA(content_amount, cache_size, p_dict)
    total_ratio = sca.totalHitRatio()

    for i in range(5, 121, 5):
        print (i)
        index.append(i)
        data.append(total_ratio)
        sca_validation = SCAValidationEx(
            content_amount, cache_size, p_dict, request_rate, i)
        data_validation.append(sca_validation.totalHitRatio())
    print(data_validation)
    # data_validation = [0.112428673342427, 0.20261753226812357, 0.2422101866416663, 0.2689436282156983, 0.28582385256037496, 0.2949111857517776, 0.30692548131609065, 0.31289325064290957, 0.31794290609920933, 0.32623924159054435, 0.3298618880057964, 0.33303990158448593, 0.3358533459249052, 0.33836362156566246, 0.34061870748426637, 0.34265670541834925, 0.3445083022503371, 0.34619852114569727, 0.34774799253942457, 0.3518315410218549, 0.35307016934848706, 0.3542161281411062, 0.355279477605182, 0.3562688449867552]
    saveToTxt(data_validation)
    plt.plot(index, data, label='model-SCA')
    plt.plot(index, data_validation, label='model-SCAV')
    plt.plot(index_txt, data_txt, '+', label='simulation', color="red")
    plt.xlabel("staleness time(s)")
    plt.ylabel("hit ratio")
    plt.axis([0,125,0,0.5])
    plt.grid(True)
    plt.legend()
    plt.show()
