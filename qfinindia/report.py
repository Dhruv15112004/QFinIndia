from qfinindia.analytics import Analytics
import pandas as pd


def _compute_metrics(chain, expiry=None):
    """
    Internal: compute all implied parameters once.
    Supports auto-expiry if not provided.
    """
    a = Analytics(chain, expiry)

    spot = a.spot
    fwd = a.forward

    metrics = {
        "spot": float(spot),
        "forward": float(fwd),
        "forward_pct": float((fwd - spot) / spot),
        "expected_move": float(a.expected_move),
        "atm_vol": float(a.atm_vol),
        "skew": float(a.skew),
        "var_5": float(a.var(0.05)),
        "var_1": float(a.var(0.01)),
        "bias": a.bias,
    }

    return metrics


def generate_report(chain, expiry=None, output="text"):
    """
    Generate QFinIndia implied market report.

    Parameters
    ----------
    chain : OptionChain
    expiry : optional
        If None, first expiry in chain is used.
    output : {"text","dict","df"}

    Returns
    -------
    str | dict | pandas.DataFrame
    """

    m = _compute_metrics(chain, expiry)

    if output == "dict":
        return m

    if output == "df":
        return pd.DataFrame([m])

    report = f"""
QFinIndia IMPLIED MARKET REPORT
--------------------------------
Spot: {m['spot']:.0f}
Forward: {m['forward']:.0f} ({m['forward_pct']*100:.2f}%)

Expected Move: ±{m['expected_move']:.0f}
ATM Vol: {m['atm_vol']:.2f}
Skew: {m['skew']:.2f}

VaR 5%: {m['var_5']:.0f}
VaR 1%: {m['var_1']:.0f}

Bias: {m['bias']}
"""
    return report.strip()
