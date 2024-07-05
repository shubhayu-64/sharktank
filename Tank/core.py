from datetime import datetime
import json
from Tank.Database.db import TankDB
from Tank.Model.schemas import InvestmentModel, PortfolioModel, TransactionModel, TransactionType


class Tank:
    def __init__(self, db: TankDB) -> None:
        self.db = db
        self.portfolio = self.db.init_portfolio()


    def make_transaction(self, asset: str, quantity: float, type: TransactionType) -> None:

        # TODO: Get current price of asset from API
        # For now, set price to 10.0
        price = 10.0

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
        # TODO: Update this to get current value of all assets
        # current_value = sum([inv.quantity * get_market_value(inv.asset) for inv in investments])
        current_value = sum([inv.quantity * price for inv in investments])
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
