from contextlib import contextmanager
from Tank.config import configs
from Tank.Database.DBModels import Base, Transaction
from Tank.Model.transactions import TransactionModel
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

    def create_transaction(self, transaction_data: TransactionModel):
        with self._get_db() as db:
            try:
                transaction_dict = transaction_data.dict()
                new_transaction = Transaction(**transaction_dict)
                print(transaction_data)
                db.add(new_transaction)
                db.commit()
                db.refresh(new_transaction)
            except Exception as e:
                db.rollback()
                raise e

            return new_transaction
    
    def read_transactions(self):
        with self._get_db() as db:
            return db.query(Transaction).all()