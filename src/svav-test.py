import math
from sympy import Symbol
from sympy import solve
from mcav.zipf import Zipf


class SCAV(object):
    # realize the SCA algorithm
    def __init__(self, amount, size, popurity_dict, rate, time):
        self._amount = amount
        self._size = size
        self._alpha = popurity_dict
        self._P = {}
        # self._P[1] = self._alpha
        self._B = {}
        self._BN = self._initializeBN()
        self._request_rate = rate
        self._staleness_time = time
        self._validation_rate = self._validationRate()
        self._validation_probability = self._validationProbability()
        self._P[1] = self._computeP1()
        self._hit_ratio = {}
        self._hitRatio()

    def hitRatio(self):
        return self._hit_ratio

    def totalHitRatio(self):
        total_hit_ratio = 0.0
        for i in range(1, self._amount + 1):
            total_hit_ratio = total_hit_ratio + \
                self._alpha[i]*self._hit_ratio[i]
        return total_hit_ratio

    def _hitRatio(self):
        for i in range(1, self._size + 1):
            print(i)
            self._computeB(i)
            i = i + 1
            if i <= self._size:
                self._computeP(i)
        left = []
        right = []
        for i in range(1, self._amount+1):
            left.append(self._B[self._size][i]-self._BN[i])
            right.append(self._BN[i])
        print (left)
        print (right)
        result = solve(left, right)
        for i in range(1, self._amount+1):
            self._hit_ratio[i] = result[self._BN[i]]

    def _computeP(self, position):
        # position starts from 2
        p = {}
        molecule = []
        denominator = 0.0
        for i in range(1, self._amount + 1):
            denominator = denominator +  self._alpha[i] * (1 - self._B[position-1][i])
        for i in range(1, self._amount + 1):
            molecule = self._alpha[i] * (
                self._BN[i] - self._B[position - 1][i]
            ) * self._validation_probability[i] + self._alpha[i] * (
                1 - self._BN[i])
            p[i] = molecule / denominator

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
            vp[i] = 1 - math.pow(
                math.e, -self._validation_rate[i] * self._staleness_time)
        return vp

    # def _validationRate(self):
    #     validation_rate = self._request_rate
    #     return validation_rate

    def _validationRate(self):
        validation_rate = {}
        for i in range(1, self._amount + 1):
            i_request_rate = self._alpha[i] * self._request_rate * 0.1
            validation_rate[i] = i_request_rate
            # validation_rate[i] = i_request_rate*math.pow(math.e, -self._size/(self._request_rate*self._staleness_time))

        # validation_rate = self._request_rate * \
        #     math.pow(math.e, - self._size /
        #              self._staleness_time/self._request_rate)
        return validation_rate

    def _computeP1(self):
        P1 = {}
        for i in range(1, self._amount + 1):
            P1[i] = self._alpha[i] * self._validation_probability[
                i] * self._BN[i] + self._alpha[i] * (1 - self._BN[i])
        return P1

    def _initializeBN(self):
        BN = {}
        for i in range(1, self._amount + 1):
            BN[i] = Symbol('b' + str(i) + 'N')
        return BN


if __name__ == "__main__":
    content_amount = 100
    cache_size = 10
    request_rate = 10
    staleness_time = 20
    z = 0.8  # zipf parameter
    zipf = Zipf(content_amount, z)
    p_dict = zipf.popularity()  # popularity of the contents
    scav = SCAV(content_amount, cache_size, p_dict, request_rate, staleness_time)

    print (scav.hitRatio())
    print (scav.totalHitRatio())


    x = Symbol('x')
    y = Symbol('y')
