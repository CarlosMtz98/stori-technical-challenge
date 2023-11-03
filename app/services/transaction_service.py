import datetime
import logging
from functools import reduce

from app.models.transaction import Transaction, TransactionType, TransactionReport
from app.repository.transaction_repository import TransactionRepository
from app.utils.email.smtp_email_sender import SmtpEmailSender


class TransactionService:
    def __init__(self, transaction_repository: TransactionRepository, email_sender: SmtpEmailSender, logger):
        self.repository = transaction_repository
        self.email_sender = email_sender
        self.logger = logger if logger else logging.getLogger(__name__)

    def generate_data_report(self):
        today = datetime.datetime.today()
        transactions_list = self.repository.get_transactions()
        if len(transactions_list) == 0:
            return TransactionReport(today, 0, 0, 0, [])

        credit_trx = list(filter(lambda t: t.Type == TransactionType.CREDIT,  transactions_list))
        debit_trx = list(filter(lambda t: t.Type == TransactionType.DEBIT,  transactions_list))

        total_debit = reduce(lambda accum, trx: accum + trx.Amount, debit_trx, 0.0)
        total_credit = reduce(lambda accum, trx: accum + trx.Amount, credit_trx, 0.0)
        average_credit = total_credit / len(credit_trx)
        average_debit = total_debit / len(debit_trx)
        count_trx_by_month = self.count_transactions_by_month(transactions_list)

        return TransactionReport(today, average_debit, average_credit, total_debit - total_credit, count_trx_by_month)

    @staticmethod
    def count_transactions_by_month(transactions_list: list[Transaction]):
        trx_year = {}
        for trx in transactions_list:
            year = trx.Datetime.year
            month = trx.Datetime.month
            if year not in trx_year:
                trx_year[year] = {}
            if month not in trx_year[year]:
                trx_year[year][month] = 0
            trx_year[year][month] += 1

        return trx_year

    def send_transactions_report(self, report: TransactionReport, receivers):
        email_subject = "Transaction report"
        template_file_name = "transactions_report.html"
        report_data = report.to_dict()
        render_html_template = self.email_sender.render_template(template_file_name, report_data)

        self.email_sender.connect()
        for receiver in receivers:
            self.email_sender.send_email(receiver, email_subject, render_html_template)

            self.logger.info(f"Transactions report sent correctly to {receiver}")
        self.email_sender.disconnect()
