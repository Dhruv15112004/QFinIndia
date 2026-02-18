import numpy as np
from scipy.stats import norm


class NSEOption:
    """
    Black-Scholes option pricing adapted for Indian markets.
    Provides price and Greeks.
    """

    def __init__(self, spot, strike, rate, vol, time):
        self.S = float(spot)
        self.K = float(strike)
        self.r = float(rate)
        self.sigma = float(vol)
        self.T = float(time)

    # ---------- core terms ----------
    def _d1(self):
        return (np.log(self.S / self.K) +
                (self.r + 0.5 * self.sigma**2) * self.T) / \
               (self.sigma * np.sqrt(self.T))

    def _d2(self):
        return self._d1() - self.sigma * np.sqrt(self.T)

    # ---------- pricing ----------
    def call_price(self):
        d1 = self._d1()
        d2 = self._d2()
        return self.S * norm.cdf(d1) - \
               self.K * np.exp(-self.r * self.T) * norm.cdf(d2)

    def put_price(self):
        d1 = self._d1()
        d2 = self._d2()
        return self.K * np.exp(-self.r * self.T) * norm.cdf(-d2) - \
               self.S * norm.cdf(-d1)

    # ---------- greeks ----------
    def call_delta(self):
        return norm.cdf(self._d1())

    def put_delta(self):
        return norm.cdf(self._d1()) - 1

    def gamma(self):
        return norm.pdf(self._d1()) / \
               (self.S * self.sigma * np.sqrt(self.T))

    def vega(self):
        return self.S * norm.pdf(self._d1()) * np.sqrt(self.T)

    def call_theta(self):
        d1 = self._d1()
        d2 = self._d2()
        term1 = -self.S * norm.pdf(d1) * self.sigma / (2 * np.sqrt(self.T))
        term2 = -self.r * self.K * np.exp(-self.r * self.T) * norm.cdf(d2)
        return term1 + term2

    def put_theta(self):
        d1 = self._d1()
        d2 = self._d2()
        term1 = -self.S * norm.pdf(d1) * self.sigma / (2 * np.sqrt(self.T))
        term2 = self.r * self.K * np.exp(-self.r * self.T) * norm.cdf(-d2)
        return term1 + term2
    
        # ---------- implied volatility ----------
    def implied_volatility(self, market_price, option_type="call",
                           tol=1e-6, max_iter=100):
        """
        Compute implied volatility using Newton-Raphson.
        """

        sigma = 0.2  # initial guess

        for _ in range(max_iter):
            self.sigma = sigma

            if option_type.lower() == "call":
                price = self.call_price()
            else:
                price = self.put_price()

            diff = price - market_price

            if abs(diff) < tol:
                return sigma

            vega = self.vega()

            if vega == 0:
                break

            sigma = sigma - diff / vega

        return sigma

