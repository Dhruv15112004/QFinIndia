import numpy as np


class ScenarioAnalytics:
    """
    Market-implied scenario probabilities from risk-neutral density.
    """

    def __init__(self, strikes, density, spot):
        self.K = np.array(strikes)
        self.f = np.array(density)
        self.spot = spot

        # normalize
        self.f = self.f / np.trapz(self.f, self.K)

    def prob_below(self, level):
        mask = self.K <= level
        return np.trapz(self.f[mask], self.K[mask])

    def prob_above(self, level):
        mask = self.K >= level
        return np.trapz(self.f[mask], self.K[mask])

    def prob_between(self, low, high):
        mask = (self.K >= low) & (self.K <= high)
        return np.trapz(self.f[mask], self.K[mask])

    def expected_move_down(self):
        mask = self.K < self.spot
        prob = np.trapz(self.f[mask], self.K[mask])
        exp = np.trapz((self.spot - self.K[mask]) * self.f[mask], self.K[mask])
        return exp / prob if prob > 0 else 0

    def expected_move_up(self):
        mask = self.K > self.spot
        prob = np.trapz(self.f[mask], self.K[mask])
        exp = np.trapz((self.K[mask] - self.spot) * self.f[mask], self.K[mask])
        return exp / prob if prob > 0 else 0
    
    def tail_asymmetry(self):
        """
        Ratio of downside to upside probability mass.
        """
        down = self.prob_below(self.spot)
        up = self.prob_above(self.spot)
        return down / up if up > 0 else np.inf

    def expectation_asymmetry(self):
        """
        Ratio of expected down vs up move.
        """
        down = self.expected_move_down()
        up = self.expected_move_up()
        return down / up if up > 0 else np.inf

