from Tank.base import APIClient
import requests

class CoinGeckoAPIClient(APIClient):
    def authenticate(self):
        # CoinGecko API does not require authentication.
        pass
    
    def fetch_live_data(self, symbol, currency='inr'):
        currency = currency.lower()
        
        url = f"{self.base_url}/simple/price"
        params = {'ids': symbol, 'vs_currencies': currency}
        response = None
        try:
            response = requests.get(url, params)
            response.raise_for_status()
        except requests.exceptions.HTTPError as err:
            if response.status_code == 429:
                return {"status": "error", "code": 429, "message": "Rate limit exceeded"}
            else:
                return {"status": "error", "code": 500, "message": "Unkown error occurred"}
        except Exception as err:
            print(f"An error occurred: {err}")
            return None
        
        data = response.json()
        if symbol in data:
            return {"status": "success", "code": 200, "data": data[symbol][currency]}
        else:
            print(f"Coin {symbol} not found.")
            return None