import numpy as np

def simulate_slippage(price, volume, market_impact):
    slippage = market_impact * (volume / (volume + 1))  # Simplified slippage model
    return price * (1 + slippage)