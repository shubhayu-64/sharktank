from Tank.base import APIClient
import yfinance as yf



class YahooFinanceAPIClient(APIClient):
    def __init__(self):
        super().__init__(api_type="stock")
    
    def fetch_info(self, symbol):
        data = yf.Ticker(symbol)
        return data.info

    def fetch_live_data(self, symbol):
        data = yf.Ticker(symbol)
        intervals = ['1m','2m','5m', '15m', '30m', '60m', '90m', '1h', '1d', '5d', '1wk', '1mo', '3mo']
        current_price = data.history(interval='2m')['Close'].iloc[-1]
        return current_price
    
    def fetch_historical_data(self, symbol, start_date, end_date):
        data = yf.Ticker(symbol)
        return data.history(start=start_date, end=end_date).to_dict(orient='records')
    