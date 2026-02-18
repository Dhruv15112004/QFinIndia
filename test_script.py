from qfinindia.options.black_scholes import NSEOption
from qfinindia.volatility.smile import VolSmile
from qfinindia.volatility.surface import VolSurface
from qfinindia.volatility.analytics import SurfaceAnalytics
from qfinindia.volatility.rnd import RiskNeutralDensity
from qfinindia.volatility.distribution import DistributionAnalytics
from qfinindia.volatility.scenario import ScenarioAnalytics
from qfinindia.data.nse import NSEClient
from qfinindia.market.option_chain import OptionChain

spot = 22500
strike = 22600
rate = 0.065
vol = 0.18
time = 0.1

opt = NSEOption(spot, strike, rate, vol, time)

print("Call Price:", opt.call_price())
print("Put Price:", opt.put_price())

print("Call Delta:", opt.call_delta())
print("Put Delta:", opt.put_delta())
print("Gamma:", opt.gamma())
print("Vega:", opt.vega())
print("Call Theta:", opt.call_theta())
print("Put Theta:", opt.put_theta())

print("\n--- Implied Volatility Test ---")

market_call_price = opt.call_price()  # using our own price
iv = opt.implied_volatility(market_call_price, "call")

print("Recovered IV:", iv)
print("Original IV:", vol)

print("\n--- Volatility Smile ---")

strikes = [22000, 22200, 22400, 22600, 22800]
prices = [820, 650, 520, 410, 320]  # example market prices

smile = VolSmile(
    spot=22500,
    rate=0.065,
    time=0.05,
    strikes=strikes,
    prices=prices,
    option_type="call"
)

ivs = smile.compute_iv()
print("IVs:", ivs)

smile.plot()

print("\n--- Vol Surface ---")

strikes = [22000, 22400, 22800]
maturities = [0.02, 0.05, 0.1]

prices_matrix = [
    [950, 720, 520],   # 1W
    [820, 520, 320],   # 1M
    [650, 430, 260]    # 3M
]

surface = VolSurface(
    spot=22500,
    rate=0.065,
    maturities=maturities,
    strikes=strikes,
    prices_matrix=prices_matrix,
    option_type="call"
)

ivs = surface.compute()
print("IV Surface:\n", ivs)

surface.plot()

print("\n--- Surface Analytics ---")

analytics = SurfaceAnalytics(
    strikes=strikes,
    maturities=maturities,
    iv_surface=ivs,
    spot=22500
)

T, atm = analytics.atm_term_structure()
print("ATM Term Structure:", atm)

T, skew = analytics.skew()
print("Skew:", skew)

T, curv = analytics.curvature()
print("Curvature:", curv)

print("\n--- Risk Neutral Density ---")

rnd = RiskNeutralDensity(
    spot=22500,
    rate=0.065,
    time=0.05,
    strikes=strikes,
    prices=[820,650,520,410,320]
)

K_mid, dens = rnd.compute()
print("Density:", dens)

rnd.plot()

print("\n--- Distribution Analytics ---")

# recompute RND with more strikes
strikes = [22000, 22200, 22400, 22600, 22800]
prices = [820, 650, 520, 410, 320]

rnd = RiskNeutralDensity(
    spot=22500,
    rate=0.065,
    time=0.05,
    strikes=strikes,
    prices=prices
)

K_mid, dens = rnd.compute()

dist = DistributionAnalytics(K_mid, dens)

print("Implied Mean:", dist.mean())
print("Implied Variance:", dist.variance())
print("Implied Skewness:", dist.skewness())
print("Implied Kurtosis:", dist.kurtosis())
print("Crash Prob (<22000):", dist.crash_probability(22000))
print("\n--- Tail Risk ---")

print("5% VaR:", dist.var(0.05))
print("5% Expected Shortfall:", dist.expected_shortfall(0.05))

print("\n--- Scenario Analytics ---")

scen = ScenarioAnalytics(K_mid, dens, spot=22500)

print("Prob <22000:", scen.prob_below(22000))
print("Prob 22400–22800:", scen.prob_between(22400, 22800))
print("Prob >22800:", scen.prob_above(22800))

print("Expected Down Move:", scen.expected_move_down())
print("Expected Up Move:", scen.expected_move_up())
print("\n--- Asymmetry ---")
print("Tail Asymmetry:", scen.tail_asymmetry())
print("Expectation Asymmetry:", scen.expectation_asymmetry())

client = NSEClient()
raw = client.get_option_chain("NIFTY")

chain = OptionChain(raw)

print(chain.df.head())

# choose nearest expiry
expiry = sorted(chain.df["expiry"].unique())[0]

calls = chain.get_calls(expiry)

print("\nNearest Expiry:", expiry)
print(calls.head())
