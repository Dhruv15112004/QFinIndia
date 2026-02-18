import numpy as np


class TailRisk:

    def __init__(self, strikes, density):
        self.strikes = strikes
        self.density = density / np.trapz(density, strikes)

    @classmethod
    def from_distribution(cls, dist):
        return cls(dist.strikes, dist.density)

    def var(self, alpha=0.05):
        cdf = np.cumsum(self.density)
        cdf /= cdf[-1]
        idx = np.searchsorted(cdf, alpha)
        return self.strikes[idx]

    def expected_shortfall(self, alpha=0.05):
        var_level = self.var(alpha)
        mask = self.strikes <= var_level
        prob = np.trapz(self.density[mask], self.strikes[mask])
        loss = np.trapz(self.strikes[mask] * self.density[mask], self.strikes[mask])
        return loss / prob if prob > 0 else np.nan

    def downside_probability(self, spot):
        mask = self.strikes < spot
        return np.trapz(self.density[mask], self.strikes[mask])

    def upside_probability(self, spot):
        mask = self.strikes >= spot
        return np.trapz(self.density[mask], self.strikes[mask])
