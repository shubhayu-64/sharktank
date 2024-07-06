from datetime import datetime
from enum import Enum
from typing import List
from pydantic import BaseModel, Field

class TransactionType(str, Enum):
    BUY = "BUY"
    SELL = "SELL"

class TransactionModel(BaseModel):
    date: int = Field(default_factory=lambda: int(datetime.now().timestamp()), title="Date of Transaction", description="Date of Transaction")
    type: TransactionType = Field(..., title="Type of Transaction", description="Type of Transaction")
    asset: str = Field(..., title="Asset", description="Ticker or name of asset")
    quantity: float = Field(..., title="Quantity", description="Quantity of asset")
    price: float = Field(..., title="Price", description="Price of each asset")
    fees: float = Field(default=0.0, title="Fees", description="Fees of transaction")
    amount: float = Field(..., title="Amount", description="Amount of transaction")


class InvestmentModel(BaseModel):
    portfolio_id: int = Field(..., title="Portfolio ID", description="ID of portfolio")
    asset: str = Field(..., title="Asset", description="Ticker or name of asset")
    quantity: float = Field(..., title="Quantity", description="Quantity of asset")
    average_price: float = Field(..., title="Average Price", description="Average price of asset")
    

# Update InvestmentModel | Picked from suggestions
class PortfolioModel(BaseModel):
    liquid_cash: float = Field(..., title="Liquid Cash", description="Liquid cash available")
    net_worth: float = Field(..., title="Net Worth", description="Net worth of portfolio")
    portfolio_value: float = Field(..., title="Portfolio Value", description="Value of portfolio")
    portfolio_composition: str = Field(..., title="Portfolio Composition", description="Composition of portfolio")
    portfolio_returns: float = Field(..., title="Portfolio Returns", description="Returns of portfolio")
    portfolio_risk: float = Field(..., title="Portfolio Risk", description="Risk of portfolio")
    
    # Might want to bring this back
    # investments: List[InvestmentModel] = Field(..., title="Investments", description="List of investments")