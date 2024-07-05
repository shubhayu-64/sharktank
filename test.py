from datetime import datetime
from Tank.Database.db import TankDB
from Tank.Model.schemas import TransactionModel, TransactionType
from Tank.base import APIClientFactory

from config import configs

import time
from Tank.Clients.coindcx_client import CoinDCXAPIClient
from Tank.core import Tank

def test():
    
    factory = APIClientFactory()
    coindcx_client = CoinDCXAPIClient()
    factory.register_client('coindcx', coindcx_client)

    symbol = "MATIC"
    timeSpan = configs["timeSpan"]
    
    client = factory.get_client('coindcx')
    current_price = client.get_current_price(symbol)
    # historical_data = client.fetch_historical_data(ticker, timeSpan)
    # print("Historical Data:")
    # print(historical_data)

    print("Live Data:")
    for _ in range(5):  # Not looping infinite times
        live_data = client.get_current_price(symbol)
        print(live_data)
        
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
        print(f"Inserted Transaction ID: {new_transaction.id}")
    except Exception as e:
        print(f"Failed to insert transaction: {e}")

    # Retrieve all transactions
    transactions = tank_db.read_transactions()
    for transaction in transactions:
        print(transaction.id, transaction.date, transaction.type, transaction.asset, transaction.quantity, transaction.price, transaction.fees)
        

def test_tank():
    tank_db = TankDB()

    tank = Tank(tank_db)

    # Example usage of Tank class
    tank.make_transaction(type=TransactionType.BUY, asset="AAPL", quantity=10)
    tank.make_transaction(type=TransactionType.BUY, asset="AAPL", quantity=5)

    print("\n\nTEST COMPLETED SUCCESSFULLY")


if __name__ == "__main__":
    test()
    # test_db()

    # test_tank()

