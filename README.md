# QFinIndia

**QFinIndia** is a Python library for extracting market-implied information from option chains.

It provides volatility smile, risk-neutral density (RND), implied distribution, tail risk (VaR/CVaR), and directional bias from options data.

Designed for quant research, derivatives analytics, and market microstructure studies.

---

# 🚀 Installation

```bash
pip install qfinindia
from qfinindia import SyntheticChain, generate_report

chain = SyntheticChain(
    spot=24000,
    expiry="2026-06-25"
).build()

print(generate_report(chain))
QFinIndia IMPLIED MARKET REPORT
--------------------------------
Spot: 24000
Forward: 24503 (2.10%)

Expected Move: ±182
ATM Vol: 0.13
Skew: 0.55

VaR 5%: 24342
VaR 1%: 23940

Bias: Bullish
📊 Core Concepts

QFinIndia converts an option chain into:

Volatility smile

Risk-neutral density

Implied price distribution

Tail risk metrics

Directional market bias

The workflow:

OptionChain → Smile → RND → Distribution → Tail Risk → Report
🧱 Build Option Chains
Synthetic Chain (built-in)
from qfinindia import SyntheticChain

chain = SyntheticChain(
    spot=24000,
    expiry="2026-06-25",
    strike_range=(20000, 28000, 250),
    base_iv=0.13,
    smile=0.35,
    time_value=160,
    r=0.06,
    T=120/365
).build()

From DataFrame

Required columns:

type, strike, expiry, price, iv, oi

from qfinindia import OptionChain

chain = OptionChain.from_dataframe(df, underlying=24000)

📈 Unified Analytics Interface
from qfinindia import Analytics

a = Analytics(chain)

print(a.forward)
print(a.expected_move)
print(a.skew)
print(a.atm_vol)
print(a.var(0.05))
print(a.cvar(0.05))
print(a.bias)

📑 Implied Market Report
Text
from qfinindia import generate_report
print(generate_report(chain))

Dictionary
generate_report(chain, output="dict")

DataFrame
generate_report(chain, output="df")

📉 Plotting Helpers
from qfinindia import plot_smile, plot_rnd, plot_distribution

plot_smile(chain)
plot_rnd(chain)
plot_distribution(chain)

📊 Available Metrics

QFinIndia extracts:

Forward price

Expected move

ATM volatility

Skew

Variance

Risk-neutral density

Implied distribution

VaR

CVaR

Directional bias
🧪 Example: Full Analytics
from qfinindia import SyntheticChain, Analytics

chain = SyntheticChain(24000, "2026-06-25").build()
a = Analytics(chain)

print("Forward:", a.forward)
print("Move:", a.expected_move)
print("Skew:", a.skew)
print("VaR 5%:", a.var(0.05))
print("Bias:", a.bias)

🏗 Architecture
OptionChain
   ├─ VolSmile
   ├─ RND
   ├─ Distribution
   └─ TailRisk
         ↓
      Analytics
         ↓
     Report / Plots

     🎯 Use Cases

Options market sentiment

Implied distribution research

Risk-neutral density estimation

Volatility surface studies

Tail risk estimation

Quant trading signals

🛣 Roadmap

Multi-expiry surfaces

SABR calibration

Live NSE data loader

Surface arbitrage checks

Greeks extraction

🤝 Contributing

Pull requests and issues welcome.

📜 License

MIT License

👨‍💻 Author

Dhruv Maheshwari
Quant & Derivatives Analytics