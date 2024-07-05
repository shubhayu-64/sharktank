from contextlib import contextmanager
from Tank.config import configs
from Tank.Database.DBModels import Base, Investment, Portfolio, Transaction
from Tank.Model.schemas import InvestmentModel, PortfolioModel, TransactionModel
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

class TankDB:
    def __init__(self) -> None:
        database_path = f"sqlite:///{configs['DATABASE_NAME']}.db"
        self.engine = create_engine(database_path, echo=True)
        Base.metadata.create_all(self.engine)
        self.session_local = sessionmaker(bind=self.engine)

    @contextmanager
    def _get_db(self):
        db = self.session_local()
        try:
            yield db
        finally:
            db.close()
    
    def init_portfolio(self) -> Portfolio:
        portfolio = self.get_portfolio()
        if not portfolio:
            portfolio_data = PortfolioModel(
                net_worth=0.0,
                portfolio_value=0.0,
                portfolio_performance=0.0,
                portfolio_composition="{}",
                portfolio_returns=0.0,
                portfolio_risk=0.0
            )
            portfolio = self.add_portfolio(portfolio_data)
        return portfolio

    def create_transaction(self, transaction_data: TransactionModel) -> Transaction:
        with self._get_db() as db:
            try:
                new_transaction = Transaction(**(transaction_data.dict()))
                db.add(new_transaction)
                db.commit()
                db.refresh(new_transaction)
            except Exception as e:
                db.rollback()
                raise e

            return new_transaction
    
    def read_transactions(self) -> list[Transaction]:
        with self._get_db() as db:
            return db.query(Transaction).all()
    
    
    def add_investment(self, investment_data: InvestmentModel) -> Investment:
        with self._get_db() as db:
            try:
                new_investment = Investment(**(investment_data.dict()))
                db.add(new_investment)
                db.commit()
                db.refresh(new_investment)
            except Exception as e:
                db.rollback()
                raise e

            return new_investment
    
    def read_investments(self):
        with self._get_db() as db:
            return db.query(Investment).all()
    

    def update_investment(self, asset: str, new_quantity: float, new_average_price: float):
        with self._get_db() as db:
            try:
                investment = db.query(Investment).filter_by(asset=asset).first()
                if investment:
                    investment.quantity = new_quantity
                    investment.average_price = new_average_price
                    db.commit()
                    db.refresh(investment)
                else:
                    raise ValueError(f"Investment with asset '{asset}' not found.")
            except Exception as e:
                db.rollback()
                raise e
        
    
    def add_portfolio(self, portfolio_data: PortfolioModel) -> Portfolio:
        with self._get_db() as db:
            try:
                new_portfolio = Portfolio(**(portfolio_data.dict()))
                db.add(new_portfolio)
                db.commit()
                db.refresh(new_portfolio)
            except Exception as e:
                db.rollback()
                raise e

            return new_portfolio
    
    def get_portfolio(self, portfolio_id=1):
        with self._get_db() as db:
            return db.query(Portfolio).filter_by(id=portfolio_id).first()
        
    
    def update_portfolio(self, portfolio_data: PortfolioModel):
        with self._get_db() as db:
            try:
                portfolio = db.query(Portfolio).first()
                if portfolio:
                    fields_to_update = ['net_worth', 'portfolio_value', 'portfolio_performance', 'portfolio_composition', 'portfolio_returns', 'portfolio_risk']
                    for field in fields_to_update:
                        setattr(portfolio, field, getattr(portfolio_data, field))
                    db.commit()
                    db.refresh(portfolio)
                else:
                    raise ValueError("Portfolio record not found.")
            except Exception as e:
                db.rollback()
                raise e