import numpy as np


class Distribution:

    def __init__(self, strikes, density):
        self.strikes = strikes
        self.density = density / np.trapz(density, strikes)

    @classmethod
    def from_rnd(cls, rnd):
        return cls(rnd.strikes, rnd.density)

    def mean(self):
        return np.trapz(self.strikes * self.density, self.strikes)

    def variance(self):
        m = self.mean()
        return np.trapz((self.strikes - m)**2 * self.density, self.strikes)

    def std(self):
        return np.sqrt(self.variance())

    def skew(self):
        m = self.mean()
        s = self.std()
        return np.trapz(((self.strikes - m)/s)**3 * self.density, self.strikes)

    def kurtosis(self):
        m = self.mean()
        s = self.std()
        return np.trapz(((self.strikes - m)/s)**4 * self.density, self.strikes)
