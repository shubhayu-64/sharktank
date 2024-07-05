import time
import logging

from config import configs
from Tank.core import Tank
from datetime import datetime
import random
from Tank.Database.db import TankDB
from Tank.base import APIClientFactory
from logging_config import setup_logging 
from Tank.Clients.coindcx_client import CoinDCXAPIClient
from Tank.Model.schemas import TransactionModel, TransactionType

setup_logging() # Set up logging configuration

# logger = logging.getLogger(__name__) 

def test():
    
    factory = APIClientFactory()
    coindcx_client = CoinDCXAPIClient()
    factory.register_client('coindcx', coindcx_client)

    ticker = 'I-MATIC_INR'
    symbol = "MATIC"
    timeSpan = configs["timeSpan"]
    
    client = factory.get_client('coindcx')
    try:
        current_price = client.get_current_price(symbol)
        logging.info(f"Fetched current price of {symbol}: {current_price}")
    except Exception as e:
        logging.error(f"Error in fetching current price for {symbol}: {e}")
        return
    
    try:
        historical_data = client.fetch_historical_data(ticker, timeSpan)
        logging.info(f"Fetched historical data for {ticker}")
    except Exception as e:
        logging.error(f"Error in fetching historical data for {ticker}: {e}")
        return        
        

    print("Live Data:")
    for _ in range(5):  # Not looping infinite times
        try:
            live_data = client.get_current_price(symbol)
            logging.info(f"Fetched current price of {symbol}: {live_data}")
        except Exception as e:
            logging.error(f"Error in fetching current price for {symbol}: {e}")
            return            
        
        time.sleep(1)

def test_db():
    data = {
        "date": int(datetime.now().timestamp()),
        "type": TransactionType.BUY,
        "asset": "GOOGL",
        "quantity": 10,
        "price": 100,
        "fees": 0.1
    }
    data["amount"] = data["quantity"] * data["price"] + data["fees"]

    data = TransactionModel(**data)
    tank_db = TankDB()
    # Insert a transaction using the insert_transaction method
    try:
        new_transaction = tank_db.create_transaction(data)
        # print(f"Inserted Transaction ID: {new_transaction.id}")
        logging.info(f"Inserted Transaction ID: {new_transaction.id}")
    except Exception as e:
        logging.error(f"Failed to insert transaction: {e}")
        # print(f"Failed to insert transaction: {e}")
        return        

    # Retrieve all transactions
    try:
        transactions = tank_db.read_transactions()
        logging.info(f"All DB transactions retreived at {datetime.now()}")
    except Exception as e:
        logging.error(f"Failed to retrieve transactions: {e}")
        # print(f"Failed to retrieve transactions: {e}")
        return
    
    for transaction in transactions:
        print(transaction.id, transaction.date, transaction.type, transaction.asset, transaction.quantity, transaction.price, transaction.fees)
        

def test_tank():
    # Initialize TankDB and APIClientFactory
    tank_db = TankDB()
    client_factory = APIClientFactory()
    coindcx_client = CoinDCXAPIClient()
    client_factory.register_client('coindcx', coindcx_client)

    # Initialize Tank with TankDB and APIClientFactory
    tank = Tank(tank_db, client_factory, 'coindcx')

    # Example usage of Tank class
    # tank.make_transaction(type=TransactionType.BUY, asset="AAPL", quantity=10)
    # tank.make_transaction(type=TransactionType.BUY, asset="AAPL", quantity=5)

    tickers = ["BONK", "MATIC", "ZRO", "NEAR", "NEST"]

    for _ in range(1):
        for ticker in tickers:
            try:
                # current_price = tank.api_client.get_current_price(ticker)
                transaction_type = random.choice(list(TransactionType))
                quantity = random.randint(10, 30)
                tank.make_transaction(asset=ticker, quantity=quantity, type=transaction_type)
            
            except ValueError as e:
                print(f"Error fetching current price for {ticker}: {str(e)}")
                continue

    print("\n\nTEST COMPLETED SUCCESSFULLY")


if __name__ == "__main__":
    test()
    # test_db()

    # test_tank()

