from mcav.zipf import Zipf
from math import e, pow


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
            p[i] = self._validation_probability[i][
                position] * molecule / denominator

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
                # vp[j] = 1 - pow(
                #     e, -self._validation_rate[i] * self._staleness_time *
                #     (1 - pow(e, -(j - 1))))
                vp[j] = 1 - pow(
                    e, -self._validation_rate[i] * self._staleness_time * j /
                    self._size)
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
    content_amount = 1000
    cache_size = 20
    request_rate = 10
    staleness_time = 20
    z = 0.8  # zipf parameter
    zipf = Zipf(content_amount, z)
    p_dict = zipf.popularity()  # popularity of the contents
    scav = SCAV(content_amount, cache_size, p_dict, request_rate,
                staleness_time)

    # print(scav.hitRatio())
    print(scav.totalHitRatio())
