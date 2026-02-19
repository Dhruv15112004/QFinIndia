from qfinindia.volatility.rnd import RND
from qfinindia.volatility.distribution import Distribution
from qfinindia.volatility.tailrisk import TailRisk
from qfinindia.volatility.vol_metrics import VolMetrics


class Analytics:
    """
    Unified analytics interface for option chains.
    """

    def __init__(self, chain, expiry=None):
        self.chain = chain

        if expiry is None:
            expiry = chain.expiries()[0]

        self.expiry = expiry

        self.rnd = RND.from_chain(chain, expiry)
        self.dist = Distribution.from_rnd(self.rnd)
        self.tail = TailRisk.from_distribution(self.dist)
        self.vm = VolMetrics(chain)

    # ---- core metrics ----
    @property
    def spot(self):
        return self.chain.underlying

    @property
    def forward(self):
        return self.dist.mean()

    @property
    def expected_move(self):
        return self.dist.std()

    @property
    def skew(self):
        return self.dist.skew()

    @property
    def atm_vol(self):
        return self.vm.atm_vol()

    # ---- tail ----
    def var(self, q=0.05):
        return self.tail.var(q)

    def cvar(self, q=0.05):
        return self.tail.expected_shortfall(q)

    # ---- bias ----
    @property
    def bias(self):
        if self.forward > self.spot:
            return "Bullish"
        if self.forward < self.spot:
            return "Bearish"
        return "Neutral"
