import numpy as np
from scipy.interpolate import CubicSpline


class RND:

    def __init__(self, strikes, density):
        self.strikes = strikes
        self.density = density

    @classmethod
    def from_chain(cls, chain, expiry, option_type="C"):
        sub = chain.expiry(expiry)

        if option_type == "C":
            sub = sub.calls()
        else:
            sub = sub.puts()

        df = sub.to_dataframe().sort_values("strike")

        K = df["strike"].values
        C = df["price"].values

        # spline price curve
        spline = CubicSpline(K, C)

        # second derivative (Breeden-Litzenberger)
        K_grid = np.linspace(K.min(), K.max(), 200)
        second_deriv = spline(K_grid, 2)

        density = np.maximum(second_deriv, 0)

        return cls(K_grid, density)

    def plot(self):
        import matplotlib.pyplot as plt
        plt.figure(figsize=(6,4))
        plt.plot(self.strikes, self.density)
        plt.xlabel("Strike")
        plt.ylabel("Density")
        plt.title("Risk-Neutral Density")
        plt.show()
