from datetime import datetime
from pydantic import BaseModel, Field

class TransactionModel(BaseModel):
    date: int = Field(..., title="Date of Transaction", description="Date of Transaction")
    type: str = Field(..., title="Type of Transaction", description="Type of Transaction")
    asset: str = Field(..., title="Asset", description="Ticker or name of asset")
    quantity: float = Field(..., title="Quantity", description="Quantity of asset")
    price: float = Field(..., title="Price", description="Price of each asset")
    fees: float = Field(default=0.0, title="Fees", description="Fees of transaction")