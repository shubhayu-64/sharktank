"""
Project: Shark Tank
Developer: Shubhayu Majumdar <shubhayumajumdar64@gmail.com>
// Unless it doesn't work, then I have no idea who wrote it.

Description: This is a parody project where the plan is to make a bot called shark invest into some stocks, 
crypto and trade on it using ML and basic algorithms. All trades will be on paper and no real trades will be made. 

There will be 2 major parts called the Shark and the Tank. The Shark will be the bot that will invest in stocks
and the Tank will be responsible for all trades and management. It will also hold the liquidity pool and the
stocks in the portfolio.

Hours: 0
version: 1.0.0
"""

from Shark.shark import shark_get_current_price
from Tank.coingecko_client import CoinGeckoAPIClient
from Tank.base import APIClientFactory, load_config

def main():
    config = load_config('config.yaml')
    factory = APIClientFactory()
    factory.register_clients_from_config(config)
    
    currency = 'inr'
    
    coin = 'bitcoin'
    shark_get_current_price(coin, currency)

if __name__ == "__main__":
    main()