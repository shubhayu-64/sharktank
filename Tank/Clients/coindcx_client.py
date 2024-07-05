import requests
import pandas as pd
import numpy as np
from Tank.base import APIClient

class CoinDCXAPIClient(APIClient):
    def __init__(self):
        super().__init__(api_type="stock")

        self.market_data = "https://public.coindcx.com/market_data/candles"
        self.tickers = "https://api.coindcx.com/exchange/ticker"
        self.market_details = "https://api.coindcx.com/exchange/v1/markets_details"
    

    def _validate_ticker(self, ticker: str) -> dict:
        response = requests.get(self.market_details)
        data = response.json()
        for item in data:
            if item['target_currency_short_name'] == ticker:
                return item
        raise ValueError(f"Invalid ticker: {ticker}")
    
    def get_current_price(self, ticker: str):
        validated_ticker = self._validate_ticker(ticker)
        response = requests.get(self.tickers)
        data = response.json()
        try:
            return next(float(item['last_price']) for item in data if item['market'] == validated_ticker['symbol'])
        except StopIteration:
            raise ValueError(f"No live data found for ticker: {ticker}")
        
    def fetch_live_data(self, symbol):
        url = self.tickers  
        response = requests.get(url)
        data = response.json()
        for item in data:
            if item['market'] == symbol:
                return float(item['last_price'])
        raise ValueError(f"No live data found for symbol: {symbol}")
    
    def fetch_historical_data(self, ticker: str, time_span: int, interval: str = "1m"):

        valid_intervals = ['1m','5m','15m','30m','1h','2h','4h','6h','8h','1d','3d','1w','1M']
        if interval not in valid_intervals:
            raise ValueError(f"Invalid interval: {interval}. Valid intervals are: {valid_intervals}")

        url = f"{self.market_data}?pair={ticker}&interval={interval}&limit={time_span}"

        try: 
            response = requests.get(url)
            data = response.json()

            # Only take OHLC data
            data = pd.DataFrame(data, columns=["open", "high", "low", "close"])
            data = np.array(data)
            return data

        except Exception as e: 
            raise ValueError(f"Error in fetching historical data for {ticker}: {e}")
        