from typing import Optional

class APIClient:
    VALID_API_TYPES = ["stock", "crypto"]

    def __init__(self, base_url: Optional[str] = None, api_key: Optional[str] = None, api_type: Optional[str] = None):
        self.base_url = base_url
        self.api_key = api_key
        if api_type not in self.VALID_API_TYPES:
            raise ValueError(f"Invalid api_type '{api_type}'. Must be one of {self.VALID_API_TYPES}.")
        self.api_type = api_type
    
    def authenticate(self):
        raise NotImplementedError("This method should be overridden by subclasses")
    
    def fetch_info(self, symbol):
        raise NotImplementedError("This method should be overridden by subclasses")
    
    def fetch_live_data(self, symbol):
        raise NotImplementedError("This method should be overridden by subclasses")
    
    def fetch_historical_data(self, symbol, start_date, end_date):
        raise NotImplementedError("This method should be overridden by subclasses")



class APIClientFactory:
    def __init__(self):
        self.clients = {}
    
    def register_client(self, name, client):
        self.clients[name] = client
    
    def get_client(self, name):
        client = self.clients.get(name)
        if not client:
            raise ValueError(f"No client registered under name: {name}")
        return client
    