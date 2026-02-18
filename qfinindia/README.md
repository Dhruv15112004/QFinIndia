# QFinIndia

QFinIndia is an open-source quantitative finance library that extracts 
risk-neutral distributions, volatility surfaces, and implied market outlook 
from NSE index options using a universal OptionChain architecture.

## Installation
pip install qfinindia

## Example
from qfinindia import OptionChain, generate_report

chain = OptionChain.from_nse(json_data)
print(generate_report(chain, "2026-03-27"))
