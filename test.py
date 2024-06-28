import time
from Tank.base import APIClientFactory, load_config
from Tank.coindcx_client import CoinDCXAPIClient

def main():
    config = load_config('config.yaml')
    print(config)
    
    factory = APIClientFactory()

    coindcx_client = CoinDCXAPIClient(config['api_clients']['coindcx']['base_url'], config['api_clients']['coindcx']['live_price_url'])
    factory.register_client('coindcx', coindcx_client)

    ticker = 'I-MATIC_INR'
    symbol = "MATICINR"
    timeSpan = 60
    
    client = factory.get_client('coindcx')
    historical_data = client.fetch_historical_data(ticker, timeSpan)
    print("Historical Data:")
    print(historical_data)

    print("Live Data:")
    for count in range(5):  # Not looping infinite times
        live_data = client.fetch_live_data(symbol)
        print(live_data)
        
        time.sleep(1)

if __name__ == "__main__":
    main()
