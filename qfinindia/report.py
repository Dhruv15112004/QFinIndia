from qfinindia.volatility.rnd import RND
from qfinindia.volatility.distribution import Distribution
from qfinindia.volatility.tailrisk import TailRisk
from qfinindia.volatility.vol_metrics import VolMetrics


def generate_report(chain, expiry):
    rnd = RND.from_chain(chain, expiry)
    dist = Distribution.from_rnd(rnd)
    tail = TailRisk.from_distribution(dist)
    vm = VolMetrics(chain)

    spot = chain.underlying
    fwd = dist.mean()
    move = dist.std()

    report = f"""
QFinIndia IMPLIED MARKET REPORT
--------------------------------
Spot: {spot:.0f}
Forward: {fwd:.0f} ({(fwd-spot)/spot*100:.2f}%)

Expected Move: ±{move:.0f}
ATM Vol: {vm.atm_vol():.2f}
Skew: {dist.skew():.2f}

VaR 5%: {tail.var(0.05):.0f}
VaR 1%: {tail.var(0.01):.0f}

Bias: {"Bullish" if fwd>spot else "Bearish" if fwd<spot else "Neutral"}
"""
    return report
