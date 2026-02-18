import numpy as np


class SurfaceAnalytics:
    """
    Quantitative analytics on implied volatility surface.
    """

    def __init__(self, strikes, maturities, iv_surface, spot):
        self.strikes = np.array(strikes)
        self.maturities = np.array(maturities)
        self.iv = np.array(iv_surface)
        self.spot = spot

    # ---------- ATM term structure ----------
    def atm_term_structure(self):
        idx = np.argmin(np.abs(self.strikes - self.spot))
        return self.maturities, self.iv[:, idx]

    # ---------- skew slope ----------
    def skew(self):
        slopes = []
        for row in self.iv:
            slope = np.polyfit(self.strikes, row, 1)[0]
            slopes.append(slope)
        return self.maturities, np.array(slopes)

    # ---------- curvature ----------
    def curvature(self):
        curv = []
        for row in self.iv:
            quad = np.polyfit(self.strikes, row, 2)[0]
            curv.append(quad)
        return self.maturities, np.array(curv)
