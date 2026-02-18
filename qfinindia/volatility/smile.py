import numpy as np
import matplotlib.pyplot as plt

class VolSmile:

    
    def __init__(self, strikes, iv, underlying=None, expiry=None):
        self.strikes = np.array(strikes)
        self.iv = np.array(iv)
        self.underlying = underlying
        self.expiry = expiry

    @classmethod
    def from_chain(cls, chain, expiry=None, option_type="C"):
        sub = chain

        if expiry is not None:
            sub = sub.expiry(expiry)

        if option_type == "C":
            sub = sub.calls()
        else:
            sub = sub.puts()

        df = sub.to_dataframe().dropna(subset=["iv"])

        return cls(
            strikes=df["strike"].values,
            iv=df["iv"].values,
            underlying=chain.underlying,
            expiry=expiry
        )
    
    
    def plot(self):
        plt.figure(figsize=(6,4))
        plt.plot(self.strikes, self.iv, marker="o")
        plt.xlabel("Strike")
        plt.ylabel("Implied Volatility")
        plt.title(f"Volatility Smile ({self.expiry})")
        plt.show()
