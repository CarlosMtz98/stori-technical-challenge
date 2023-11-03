import string
from datetime import datetime

from app.models.transaction import Transaction, TransactionType
from app.utils.file_reader.csv_file_reader import CSVFileReader


class TransactionRepository:
    def __init__(self, directory_path):
        self.directory_path = directory_path
        self.transactions = []

    def get_data(self):
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
            self.transactions.append(Transaction(id, date, amount, transaction_type))

    def get_transactions(self):
        return self.transactions

    @staticmethod
    def get_transaction_type(symbol: string) -> TransactionType:
        if symbol == '+':
            return TransactionType.DEBIT
        if symbol == '-':
            return TransactionType.CREDIT
