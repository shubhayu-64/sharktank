# Shark/shark.py

"""
Plan is to:
- Get data from Tank and sort tickers based on best to worst
- Make BUY and SELL calls
- Decide if trade should be short or long
- Split available liquidity pool into risk levels and invest accordingly

"""

from Tank.tank import get_current_price

def shark_get_current_price(coin, currency='inr'):
    res = get_current_price(coin, currency)
    if res and res.get("status") == "error":
        print(f"Error code {res.get('code')}: {res.get('message')}")
    elif res and res.get("status") == "success":
        print(f"Current price of {coin}: {res.get('data')}")
    else:
        print(f".")
