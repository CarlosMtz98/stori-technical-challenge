import calendar
import datetime
from enum import Enum


class TransactionType(Enum):
    DEBIT = 1
    CREDIT = 2


class Transaction:
    def __init__(self, transaction_id: int, date: datetime, amount: float, transaction_type: TransactionType):
        self.Id = transaction_id
        self.Amount = amount
        self.Datetime = date
        self.Type = transaction_type


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
