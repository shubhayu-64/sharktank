from typing import Optional
import yaml


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
    
    def register_clients_from_config(self, config):
        for name, client_info in config['api_clients'].items():
            client_class = globals()[client_info['class']]
            if 'api_key' in client_info:
                client_instance = client_class(client_info['base_url'], client_info['api_key'])
            else:
                client_instance = client_class(client_info['base_url'])
            self.register_client(name, client_instance)


def load_config(file_path):
    with open(file_path, 'r') as file:
        config = yaml.safe_load(file)
    return config