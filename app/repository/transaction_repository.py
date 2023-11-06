import string
from datetime import datetime

from app.models.transaction import Transaction, TransactionType
from app.repository.repository_interface import IRepository
from app.utils.file_reader.csv_file_reader import CSVFileReader


class TransactionRepository(IRepository):
    def __init__(self, database_session, directory_path):
        self.session = database_session,
        self.directory_path = directory_path
        self.transactions = {}

    def load_static_data(self):
        reader = CSVFileReader(self.directory_path)
        data = reader.read_csv_as_dict()
        for item in data:
            id = item.get("AccountId")
            datetime_str = item.get("Datetime")
            date = datetime.strptime(datetime_str, '%Y-%m-%d %H:%M:%S')
            amount_with_type = item.get("Transaction")
            type_symbol = amount_with_type[0]
            transaction_type = self.get_transaction_type(type_symbol)
            amount = float(amount_with_type[1::])
            if not self.get_by_id(id):
                self.transactions[id] = Transaction(id, date, amount, transaction_type)

    def get_by_id(self, id):
        if id not in self.transactions:
            return None
        return self.transactions[id]

    def get_all(self):
        return self.session[0].query(Transaction).all()

    @staticmethod
    def get_transaction_type(symbol: string) -> TransactionType:
        if symbol == '-':
            return TransactionType.DEBIT
        if symbol == '+':
            return TransactionType.CREDIT

    def create(self, item):
        self.session.add(item)
        self.session.commit()

    def update(self, item):
        self.session.merge(item)
        self.session.commit()

    def delete(self, id):
        transaction = self.get_by_id(id)
        if transaction:
            self.session.delete(transaction)
            self.session.commit()
