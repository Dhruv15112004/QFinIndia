class MarketIntelligence:

    def __init__(self, chain, dist, tail):
        self.chain = chain
        self.dist = dist
        self.tail = tail

    @classmethod
    def from_metrics(cls, chain, dist, tail):
        return cls(chain, dist, tail)

    def forward(self):
        return self.dist.mean()

    def expected_move(self):
        return self.dist.std()

    def skew(self):
        return self.dist.skew()

    def var5(self):
        return self.tail.var(0.05)

    def var1(self):
        return self.tail.var(0.01)

    def bias(self):
        fwd = self.forward()
        spot = self.chain.underlying
        diff = (fwd - spot) / spot

        if diff > 0.002:
            return "Bullish"
        elif diff < -0.002:
            return "Bearish"
        else:
            return "Neutral"

    def summary(self):
        spot = self.chain.underlying
        fwd = self.forward()
        move = self.expected_move()

        return f"""
NIFTY IMPLIED OUTLOOK
---------------------
Spot: {spot:.0f}
Forward: {fwd:.0f} ({(fwd-spot)/spot*100:.2f}%)
Expected Move: ±{move:.0f}
Skew: {self.skew():.2f}

VaR 5%: {self.var5():.0f}
VaR 1%: {self.var1():.0f}

Bias: {self.bias()}
"""
