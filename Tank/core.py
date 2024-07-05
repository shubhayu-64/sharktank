from datetime import datetime
import json
from Tank.Database.db import TankDB
from Tank.Model.schemas import InvestmentModel, PortfolioModel, TransactionModel, TransactionType
from Tank.base import APIClientFactory


class Tank:
    def __init__(self, db: TankDB, client_factory: APIClientFactory, client_name: str) -> None:
        self.db = db
        self.portfolio = self.db.init_portfolio()
        self.api_client = client_factory.get_client(client_name)

    def make_transaction(self, asset: str, quantity: float, type: TransactionType) -> None:

        # Validate transaction
        if type == TransactionType.SELL:
            investment = next((inv for inv in self.db.read_investments() if inv.asset == asset), None)
            if not investment:
                print(f"Cannot sell {asset}. Asset not found in investments.")
                return
            if quantity > investment.quantity:
                print(f"Cannot sell {quantity} units of {asset}. Only {investment.quantity} units available.")
                return

        try:
            price = self.api_client.get_current_price(asset)
        except ValueError as e:
            print(f"Error fetching current price for {asset}: {str(e)}")
            return

        # Calculate amount
        # TODO: Update with fees. Add for buy and subtract for sell
        amount = quantity * price if type == TransactionType.BUY else quantity * price

        transaction = {
            "type": type,
            "asset": asset,
            "quantity": quantity,
            "price": price,
            "amount": amount
        }
        transaction_data = TransactionModel(**transaction)
        self.db.create_transaction(transaction_data)

        # Update investments
        investment = self.db.read_investments()
        investment = next((inv for inv in investment if inv.asset == asset), None)
        if not investment:
            investment_data = InvestmentModel(portfolio_id=self.portfolio.id, asset=asset, quantity=0, average_price=0.0)
            investment = self.db.add_investment(investment_data)

        if type == TransactionType.BUY:
            total_quantity = investment.quantity + quantity
            total_cost = (investment.quantity * investment.average_price) + amount
            new_average_price = total_cost / total_quantity if total_quantity != 0 else 0.0
        elif type == TransactionType.SELL:
            total_quantity = investment.quantity - quantity
            total_cost = (investment.quantity * investment.average_price) - amount
            new_average_price = total_cost / total_quantity if total_quantity != 0 else 0.0

        self.db.update_investment(asset, total_quantity, new_average_price)

        # Update portfolio
        investments = self.db.read_investments()
        current_values = {}
        for investment in investments:
            try:
                current_price = self.api_client.get_current_price(investment.asset)
                current_values[investment.asset] = current_price * investment.quantity
            except ValueError as e:
                print(f"Error fetching current price for {investment.asset}: {str(e)}")
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
