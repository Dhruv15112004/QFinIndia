import matplotlib.pyplot as plt
from qfinindia.volatility.rnd import RND
from qfinindia.volatility.distribution import Distribution


def plot_smile(chain, expiry=None):
    if expiry is None:
        expiry = chain.expiries()[0]

    calls = chain.calls(expiry)
    K = calls.strikes()
    IV = calls.iv()

    plt.figure()
    plt.plot(K, IV)
    plt.title("Volatility Smile")
    plt.xlabel("Strike")
    plt.ylabel("IV")
    plt.show()


def plot_rnd(chain, expiry=None):
    if expiry is None:
        expiry = chain.expiries()[0]

    rnd = RND.from_chain(chain, expiry)

    plt.figure()
    plt.plot(rnd.strikes, rnd.density)
    plt.title("Risk-Neutral Density")
    plt.xlabel("Strike")
    plt.ylabel("Density")
    plt.show()


def plot_distribution(chain, expiry=None):
    if expiry is None:
        expiry = chain.expiries()[0]

    rnd = RND.from_chain(chain, expiry)
    dist = Distribution.from_rnd(rnd)

    plt.figure()
    plt.plot(dist.strikes, dist.pdf)
    plt.title("Implied Distribution")
    plt.xlabel("Strike")
    plt.ylabel("PDF")
    plt.show()
