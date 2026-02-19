import numpy as np
import pandas as pd
from qfinindia import OptionChain


class SyntheticChain:
    """
    Build arbitrage-consistent synthetic option chains easily.
    """

    def __init__(
        self,
        spot,
        expiry,
        strike_range=(0.8, 1.2, 0.02),
        base_iv=0.15,
        smile=0.3,
        time_value=100,
        r=0.05,
        T=30/365,
    ):
        """
        strike_range:
            (low_mult, high_mult, step_mult)
            OR (min_strike, max_strike, step)
        """

        self.spot = spot
        self.expiry = expiry
        self.strike_range = strike_range
        self.base_iv = base_iv
        self.smile = smile
        self.time_value = time_value
        self.r = r
        self.T = T

    def _build_strikes(self):
        a, b, c = self.strike_range

        # multiplier mode
        if a < 5 and b < 5:
            k_min = self.spot * a
            k_max = self.spot * b
            step = self.spot * c
        else:
            k_min, k_max, step = a, b, c

        return np.arange(k_min, k_max + step, step)

    def build(self):
        strikes = self._build_strikes()
        rows = []

        for k in strikes:
            m = (k - self.spot) / self.spot
            iv = self.base_iv + self.smile * m**2

            disc_k = k * np.exp(-self.r * self.T)
            call_intr = max(self.spot - disc_k, 0)
            put_intr = max(disc_k - self.spot, 0)

            call_price = call_intr + self.time_value
            put_price = put_intr + self.time_value

            rows.append(["call", k, self.expiry, call_price, iv, 1000])
            rows.append(["put", k, self.expiry, put_price, iv, 1200])

        df = pd.DataFrame(
            rows, columns=["type", "strike", "expiry", "price", "iv", "oi"]
        )

        return OptionChain.from_dataframe(df, underlying=self.spot)
