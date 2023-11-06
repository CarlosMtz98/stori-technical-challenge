import calendar
import datetime
from enum import Enum


class TransactionType(Enum):
    DEBIT = 1
    CREDIT = 2


class Transaction:
    def __init__(self, transaction_id: int, date: datetime, amount: float, transaction_type: TransactionType, idempotency_id=None):
        self.id = transaction_id
        self.amount = amount
        self.datetime = date
        self.type = transaction_type
        self.idempotency_id = idempotency_id

    def __eq__(self, other):
        if isinstance(self, other.__class__):
            return (self.id == other.id and
                    abs(self.amount - other.amount) <= .001 and
                    self.datetime == other.datetime and
                    self.type == other.type and
                    self.idempotency_id == other.idempotency_id)
        return False


class TransactionReport:
    def __init__(self, date, avg_debit, avg_credit, total_balance, transactions_by_month):
        self.date = date,
        self.total_balance = total_balance
        self.transactions_by_month = transactions_by_month
        self.avg_debit = avg_debit
        self.avg_credit = avg_credit

    def to_dict(self):
        count_trx_by_month = []
        formatted_date = self.date[0].strftime("%d/%m/%Y")
        if self.transactions_by_month:
            for year, trx_by_month in self.transactions_by_month.items():
                for month, count_by_month in trx_by_month.items():
                    month_name = calendar.month_name[month]
                    output_val = f"Number of transactions in {month_name}, {year}: {count_by_month}"
                    count_trx_by_month.append(output_val)
        return {
            "report_date": formatted_date,
            "total_balance": "{:.2f}".format(self.total_balance),
            "avg_debit": "{:.2f}".format(self.avg_debit),
            "avg_credit": "{:.2f}".format(self.avg_credit),
            "transactions_by_month": count_trx_by_month
        }
