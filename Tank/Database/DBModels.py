from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Transaction(Base):
    __tablename__ = 'transactions'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    date = Column(Integer, nullable=False, index=True)  
    type = Column(String, nullable=False, index=True) 
    asset = Column(String, nullable=False, index=True)
    quantity = Column(Float, nullable=False)
    price = Column(Float, nullable=False)
    fees = Column(Float, nullable=False)
    amount = Column(Float, nullable=False)


# Investment class
class Investment(Base):
    __tablename__ = 'investments'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    portfolio_id = Column(Integer, ForeignKey('portfolios.id'), nullable=False, index=True)
    asset = Column(String, nullable=False, index=True)
    quantity = Column(Float, nullable=False)
    average_price = Column(Float, nullable=False)

# Portfolio class
class Portfolio(Base):
    __tablename__ = 'portfolios'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    liquid_cash = Column(Float, nullable=False)
    net_worth = Column(Float, nullable=False)
    portfolio_value = Column(Float, nullable=False)
    portfolio_composition = Column(String, nullable=False)  # Consider storing as JSON string
    portfolio_returns = Column(Float, nullable=False)
    portfolio_risk = Column(Float, nullable=False)
    investments = relationship('Investment', backref='portfolio', cascade="all, delete-orphan")
