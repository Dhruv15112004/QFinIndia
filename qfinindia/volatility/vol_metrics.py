import numpy as np


class VolMetrics:

    def __init__(self, chain):
        self.chain = chain
        self.df = chain.to_dataframe()

    def forward(self):
        # mean of RND already best proxy
        from qfinindia.volatility.distribution import Distribution
        from qfinindia.volatility.rnd import RND

        expiry = self.df["expiry"].iloc[0]
        rnd = RND.from_chain(self.chain, expiry)
        dist = Distribution.from_rnd(rnd)
        return dist.mean()

    def atm_strike(self):
        fwd = self.forward()
        strikes = self.df["strike"].values
        return strikes[np.argmin(np.abs(strikes - fwd))]

    def atm_vol(self):
        K = self.atm_strike()
        row = self.df[(self.df["strike"] == K) & (self.df["type"] == "C")]
        if len(row) == 0:
            return np.nan
        return row["iv"].iloc[0]

    def skew(self):
        fwd = self.forward()
        strikes = self.df["strike"].values
        iv = self.df["iv"].values

        left = iv[strikes < fwd]
        right = iv[strikes > fwd]

        if len(left) == 0 or len(right) == 0:
            return np.nan

        return np.mean(left) - np.mean(right)
