import json
import logging
from Tank.Database.db import TankDB
from Tank.Model.schemas import InvestmentModel, PortfolioModel, TransactionModel, TransactionType
from Tank.base import APIClientFactory
from config import configs


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
        if type == TransactionType.BUY:
            amount = self._calculate_amount(self.api_client.get_current_price(asset), quantity, type)
            portfolio = self.db.get_portfolio()
            if amount > portfolio.liquid_cash:
                logging.error(f"Not enough liquid cash to buy {quantity} units of {asset}. Available: {portfolio.liquid_cash}")
                return False
        elif type == TransactionType.SELL:
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
    
    
    def _update_portfolio(self, amount: float, type: TransactionType) -> None:
        """
            Updates the portfolio with the latest data from all current investments.

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
        
        # Fetch current liquid cash
        portfolio = self.db.get_portfolio()
        
        liquidity_pool = portfolio.liquid_cash - amount if type == TransactionType.BUY else portfolio.liquid_cash + amount
        returns = (current_value - total_cost) / total_cost * 100 if total_cost != 0 else 0

        portfolio_data = PortfolioModel(
            liquid_cash=liquidity_pool,                                                                         # This is the amount of cash available to buy more stocks              
            net_worth=current_value,                                                                            # This is the total value of the portfolio
            portfolio_value=current_value,                                                                      # This is the total I have spent on average to buy all stocks
            portfolio_composition=json.dumps({inv.asset: inv.quantity for inv in investments}),                 # This is the composition of the portfolio
            portfolio_returns=returns,                                                                          # This is the % returns of the portfolio
            portfolio_risk=5.0                                                                                  # This should be calculated based on actual risk assessment models
        )

        self.db.update_portfolio(portfolio_data)


    def make_transaction(self, asset: str, quantity: float, type: TransactionType) -> None:
        """
            Executes a transaction by validating, recording, and updating the necessary records.

            Args:
                asset (str): The symbol of the asset to be bought or sold.
                quantity (float): The quantity of the asset to be bought or sold.
                type (TransactionType): The type of transaction (BUY or SELL).
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
        self._update_portfolio(amount, type)
        
        logging.info(f"Transaction successful: {type} {quantity} units of {asset} at {price} per unit.")
