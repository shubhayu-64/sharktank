from datetime import datetime
from pprint import pprint
from Tank.Database.db import TankDB
from Tank.Model.transactions import TransactionModel
from Tank.base import APIClientFactory
from Tank.yahoofinance_client import YahooFinanceAPIClient

import time
from Tank.coindcx_client import CoinDCXAPIClient

def main():
    config = load_config('config.yaml')

    # Initialize APIClientFactory
    client_factory = APIClientFactory()
    
    # Register YahooFinanceAPIClient manually
    yahoo_finance_client = YahooFinanceAPIClient()
    client_factory.register_client('yahoo_finance', yahoo_finance_client)

    # Fetch live data for GOOGL using the registered client
    client = client_factory.get_client('yahoo_finance')
    nike_data = client.fetch_live_data('NKE')

    # nike_info = client.fetch_info('NKE')
    pprint(nike_data)

    print(config)
    
    factory = APIClientFactory()

    # coindcx_client = CoinDCXAPIClient(config['api_clients']['coindcx']['base_url'], config['api_clients']['coindcx']['live_price_url'])
    coindcx_client = CoinDCXAPIClient()
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

def test_db():
    data = {
        "date": int(datetime.now().timestamp()),
        "type": "SELL",
        "asset": "AAPL",
        "quantity": 10,
        "price": 100,
        "fees": 0.1
    }

    data = TransactionModel(**data)
    tank_db = TankDB()
    # Insert a transaction using the insert_transaction method
    try:
        new_transaction = tank_db.insert_transaction(data)
        print(f"Inserted Transaction ID: {new_transaction.id}")
    except Exception as e:
        print(f"Failed to insert transaction: {e}")

    # Retrieve all transactions
    transactions = tank_db.get_transactions()
    for transaction in transactions:
        print(transaction.id, transaction.date, transaction.type, transaction.asset, transaction.quantity, transaction.price, transaction.fees)
        

if __name__ == "__main__":
    # main()
    test_db()

