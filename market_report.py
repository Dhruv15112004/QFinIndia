from qfinindia.volatility.rnd import RiskNeutralDensity
from qfinindia.volatility.distribution import DistributionAnalytics
from qfinindia.volatility.scenario import ScenarioAnalytics

def market_view(spot, rate, time, strikes, prices):
    rnd = RiskNeutralDensity(
        spot=spot,
        rate=rate,
        time=time,
        strikes=strikes,
        prices=prices
    )

    K_mid, dens = rnd.compute()

    dist = DistributionAnalytics(K_mid, dens)
    scen = ScenarioAnalytics(K_mid, dens, spot)

    print("\nNIFTY Options-Implied Market View")
    print("---------------------------------")
    print(f"Implied Mean: {dist.mean():.2f}")
    print(f"Implied Vol (σ): {dist.variance()**0.5:.2f}")
    print(f"Skewness: {dist.skewness():.3f}")
    print(f"Kurtosis: {dist.kurtosis():.3f}")

    print(f"Prob < {spot-500}: {scen.prob_below(spot-500):.3f}")
    print(f"Expected Down Move: {scen.expected_move_down():.1f}")
    print(f"Expected Up Move: {scen.expected_move_up():.1f}")

    print(f"Tail Asymmetry: {scen.tail_asymmetry():.2f}")
    print(f"Expectation Asymmetry: {scen.expectation_asymmetry():.2f}")


if __name__ == "__main__":
    spot = 22500
    rate = 0.065
    time = 0.05

    strikes = [22000, 22200, 22400, 22600, 22800]
    prices = [820, 650, 520, 410, 320]

    market_view(spot, rate, time, strikes, prices)
