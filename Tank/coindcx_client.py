import requests
import pandas as pd
import numpy as np
from Tank.base import APIClient

class CoinDCXAPIClient(APIClient):
    def __init__(self, base_url, live_price_url):
        super().__init__()
        self.base_url = "https://public.coindcx.com"
        self.live_price_url = "https://api.coindcx.com/exchange/ticker"
    
    def authenticate(self):
        pass
    
    def fetch_live_data(self, symbol):
        url = self.live_price_url
        response = requests.get(url)
        data = response.json()
        for item in data:
            if item['market'] == symbol:
                return float(item['last_price'])
        raise ValueError(f"No live data found for symbol: {symbol}")
    
    def fetch_historical_data(self, ticker, timeSpan):
        url = f"{self.base_url}/market_data/candles?pair={ticker}&interval=1m&limit={timeSpan}"
        response = requests.get(url)
        data = response.json()
        data = pd.DataFrame(data, columns=["close"])
        data = np.array(data)
        data = data.flatten()
        return data

