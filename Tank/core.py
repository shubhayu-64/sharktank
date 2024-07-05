import json
import logging
from Tank.Database.db import TankDB
from Tank.Model.schemas import InvestmentModel, PortfolioModel, TransactionModel, TransactionType
from Tank.base import APIClientFactory


class Tank:
    def __init__(self, db: TankDB, client_factory: APIClientFactory, client_name: str) -> None:
        self.db = db
        self.portfolio = self.db.init_portfolio()
        self.api_client = client_factory.get_client(client_name)
        
    def _validate_transaction(self, asset: str, quantity: float, type: TransactionType) -> bool:
        """Validates a transaction before processing.

            This function performs the following checks:

            - For sell transactions:
                - Ensures the specified asset exists in the portfolio's investments.
                - Verifies that the sell quantity doesn't exceed the available quantity of the asset.

            Args:
                asset (str): The symbol of the asset to be bought or sold.
                quantity (float): The quantity of the asset to be bought or sold.
                type (TransactionType): The type of transaction (BUY or SELL).

            Returns:
                bool: True if the transaction is valid, False otherwise.

            Raises:
                None
        """
        if type == TransactionType.SELL:
            investment = next((inv for inv in self.db.read_investments() if inv.asset == asset), None)
            if not investment:
                logging.error(f"Cannot sell {asset}. Asset not found in investments.")
                return False
            if quantity > investment.quantity:
                logging.error(f"Cannot sell {quantity} units of {asset}. Only {investment.quantity} units available.")
                return False
        return True
    
    def _calculate_amount(self, price: float, quantity: float, type: TransactionType) -> float:
        fees = 0.0
        return quantity * price + fees if type == TransactionType.BUY else quantity * price - fees
    
    def _update_investment(self, asset: str, quantity: float, type: TransactionType, amount: float) -> None:
        investment = self.db.read_investments()
        investment = next((inv for inv in investment if inv.asset == asset), None)
        if not investment:
            investment_data = InvestmentModel(portfolio_id=self.portfolio.id, asset=asset, quantity=0, average_price=0.0)
            investment = self.db.add_investment(investment_data)

        total_quantity = investment.quantity + quantity if type == TransactionType.BUY else investment.quantity - quantity
        total_cost = (investment.quantity * investment.average_price) + amount if type == TransactionType.BUY else (investment.quantity * investment.average_price) - amount
        new_average_price = total_cost / total_quantity if total_quantity != 0 else 0.0

        self.db.update_investment(asset, total_quantity, new_average_price)
    
    
    def _update_portfolio(self) -> None:
        """
            Updates the portfolio with the latest data from all current investments.

            This method performs the following steps:
            1. Reads the current investments from the database.
            2. Fetches the current price of each investment asset.
            3. Calculates the current value of each investment.
            4. Calculates the total current value and cost of the portfolio.
            5. Updates the portfolio model with the latest net worth, portfolio value, performance, composition, returns, and risk.
            6. Saves the updated portfolio data to the database.

            Raises:
                ValueError: If there's an error fetching the current price for any investment asset.
        """
        investments = self.db.read_investments()
        current_values = {}
        for investment in investments:
            try:
                current_price = self.api_client.get_current_price(investment.asset)
                current_values[investment.asset] = current_price * investment.quantity
            except ValueError as e:
                logging.error(f"Error fetching current price for {investment.asset}: {str(e)}")
                current_values[investment.asset] = 0.0

        current_value = sum(current_values.values())
        total_cost = sum([inv.quantity * inv.average_price for inv in investments])

        portfolio_data = PortfolioModel(
            net_worth=current_value,
            portfolio_value=current_value,
            portfolio_performance=(current_value - total_cost) / total_cost * 100 if total_cost != 0 else 0,
            portfolio_composition=json.dumps({inv.asset: inv.quantity for inv in investments}),
            portfolio_returns=(current_value - total_cost) / total_cost * 100 if total_cost != 0 else 0,
            portfolio_risk=5.0  # This should be calculated based on actual risk assessment models
        )

        self.db.update_portfolio(portfolio_data)


    def make_transaction(self, asset: str, quantity: float, type: TransactionType) -> None:
        """
            Executes a transaction by validating, recording, and updating the necessary records.

            This function performs the following steps:
            1. Validates the transaction.
            2. Fetches the current price of the asset.
            3. Calculates the transaction amount.
            4. Creates and records the transaction in the database.
            5. Updates the investment record.
            6. Updates the portfolio record.

            Args:
                asset (str): The symbol of the asset to be bought or sold.
                quantity (float): The quantity of the asset to be bought or sold.
                type (TransactionType): The type of transaction (BUY or SELL).

            Returns:
                None
        """

        # Validate transaction
        if not self._validate_transaction(asset, quantity, type):
            return

        try:
            price = self.api_client.get_current_price(asset)
        except ValueError as e:
            logging.error(f"Error fetching current price for {asset}: {str(e)}")
            return

        # Calculate amount
        amount = self._calculate_amount(price, quantity, type)

        transaction_data = TransactionModel(
            type=type,
            asset=asset,
            quantity=quantity,
            price=price,
            amount=amount
        )
        self.db.create_transaction(transaction_data)

        # Update investments and portfolio
        self._update_investment(asset, quantity, type, amount)
        self._update_portfolio()
