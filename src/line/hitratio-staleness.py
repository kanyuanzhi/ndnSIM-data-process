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

def saveToTxt(hit_ratio):
    size = len(hit_ratio[0])
    keys = hit_ratio[0].keys()
    keys.sort()
    print(keys)
    with open ('./src/line/hitratio-line-data.txt','w') as f:
        for i in range(size):
            line = ""
            for j in range(len(hit_ratio)):
                line = line + str(hit_ratio[j][keys[i]]) + '\t'
            line = line + '\n'
            f.write(line)


if __name__ == "__main__":
    content_amount = 1000
    cache_size = 100
    request_rate = 10.0
    staleness_time = 50
    z = 0.8  # zipf parameter
    zipf = Zipf(content_amount, z)
    p_dict = zipf.popularity()  # popularity of the contents
    nodes = 4

    hit_ratio_txt = {0:[],1:[],2:[],3:[]}
    index_txt = []
    f = open("./src/line/hitratio-staleness.txt", "r")
    lines = f.readlines()
    for line in lines:
        item = line.split('\t')
        index_txt.append(int(item[0]))
        for i in range(nodes):
            hit_ratio_txt[i].append(float(item[i+1]))

    hit_ratio = {0:[],1:[],2:[],3:[]}
    index = []
    f = open("./src/line/hitratio-line-data.txt", "r")
    lines = f.readlines()
    for line in lines:
        item = line.split('\t')
        index.append(int(item[0]))
        for i in range(nodes):
            hit_ratio[i].append(float(item[i+1])) 

    # hit_ratio_0 = {}
    # hit_ratio_1 = {}
    # hit_ratio_2 = {}
    # hit_ratio_3 = {}

    # hit_ratio = {0:hit_ratio_0, 1:hit_ratio_1, 2:hit_ratio_2, 3:hit_ratio_3}
        
    # index = []
    # for i in range(55, 121, 5):
    #     print i
    #     index.append(i)
    #     mca = MCA(content_amount, cache_size, p_dict, request_rate, i)
    #     mca_out_rate = mca.outRate()
    #     for j in range(nodes):
    #         hit_ratio[j][i] = mca.totaHitRatio()
    #         mca = MCA(content_amount, cache_size, p_dict, request_rate, i, mca_out_rate)
    #         mca_out_rate = mca.outRate()
    #     hit_ratio[j][i] = mca.totaHitRatio()
    # print(hit_ratio)
    # saveToTxt(hit_ratio)
    for i in range(nodes):
        plt.subplot(2,2,i+1)
        plt.axis([0, 130, 0, 0.5])
        plt.plot(index, hit_ratio[i], label="node"+str(i)+"-model")
        plt.plot(index_txt, hit_ratio_txt[i], '+', label="node"+str(i)+"-simulation", color="red")
        plt.legend()
        plt.xlabel('staleness time(s)')
        plt.ylabel('hit ratio')
        plt.grid(True)
    plt.show()
 
