import requests
import pandas as pd
import numpy as np
from Tank.base import APIClient

class CoinDCXAPIClient(APIClient):
    def __init__(self):
        super().__init__(api_type="stock")

        self.market_data = "https://public.coindcx.com/market_data/candles"
        self.live_price_url = "https://api.coindcx.com/exchange/ticker"

    
    def fetch_live_data(self, symbol):
        url = self.live_price_url
        response = requests.get(url)
        data = response.json()
        for item in data:
            if item['market'] == symbol:
                return float(item['last_price'])
        raise ValueError(f"No live data found for symbol: {symbol}")
    
    def fetch_historical_data(self, ticker: str, timeSpan: int, interval: str = "1m"):

        validIntervals = ['1m','5m','15m','30m','1h','2h','4h','6h','8h','1d','3d','1w','1M']
        if interval not in validIntervals:
            raise ValueError(f"Invalid interval: {interval}. Valid intervals are: {validIntervals}")

        url = f"{self.market_data}?pair={ticker}&interval={interval}&limit={timeSpan}"

        try: 
            response = requests.get(url)
            data = response.json()

            # Only take OHLC data
            data = pd.DataFrame(data, columns=["open", "high", "low", "close"])
            data = np.array(data)
            return data

        except: 
            raise ValueError(f"Error fetching data for ticker: {ticker}")

        