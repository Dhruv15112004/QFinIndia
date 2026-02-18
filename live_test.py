import json
from qfinindia.market.option_chain import OptionChain
from qfinindia.volatility.smile import VolSmile
from qfinindia.volatility.surface import VolSurface
from qfinindia.volatility.rnd import RND
from qfinindia.volatility.distribution import Distribution
from qfinindia.volatility.tailrisk import TailRisk
from qfinindia.market.market_intelligence import MarketIntelligence
from qfinindia.volatility.vol_metrics import VolMetrics
from qfinindia.report import generate_report

# Load NSE snapshot
with open("data/nifty_option_chain.json") as f:
    raw = json.load(f)

# Universal chain
chain = OptionChain.from_nse(raw)

# Smile
smile = VolSmile.from_chain(chain, expiry="2026-03-27")

print("Underlying:", chain.underlying)
print("Strikes sample:", smile.strikes[:5])
print("IV sample:", smile.iv[:5])
smile.plot()

surface = VolSurface.from_chain(chain)

print(surface.df.head())

rnd = RND.from_chain(chain, expiry="2026-03-27")
rnd.plot()

dist = Distribution.from_rnd(rnd)

print("Mean:", dist.mean())
print("Std:", dist.std())
print("Skew:", dist.skew())
print("Kurtosis:", dist.kurtosis())

tail = TailRisk.from_distribution(dist)

print("VaR 5%:", tail.var(0.05))
print("VaR 1%:", tail.var(0.01))
print("Downside prob:", tail.downside_probability(chain.underlying))
print("Upside prob:", tail.upside_probability(chain.underlying))

mi = MarketIntelligence.from_metrics(chain, dist, tail)

print(mi.summary())

vm = VolMetrics(chain)

print("Forward:", vm.forward())
print("ATM strike:", vm.atm_strike())
print("ATM vol:", vm.atm_vol())
print("Skew slope:", vm.skew())

print(generate_report(chain, "2026-03-27"))