import app.config.logging_config
import os
import logging

from app.repository.transaction_repository import TransactionRepository
from app.services.transaction_service import TransactionService
from dotenv import load_dotenv

from app.utils.email.smtp_email_sender import SmtpEmailSender
from app.utils.file_reader.csv_file_reader import CSVFileReader


def load_recipient(file_location):
    recipient_list = []
    reader = CSVFileReader(file_location)
    data = reader.read_csv_as_dict()
    for item in data:
        recipient_list.append(item.get("email"))

    return recipient_list


if __name__ == "__main__":
    load_dotenv()
    logger = logging.getLogger('app')

    # Create transaction repository object
    transactions_file_location = 'data/transactions/transactions_example.csv'
    transaction_repository = TransactionRepository(transactions_file_location)
    # The data load is for reading values from a static file such as the transaction_example.csv
    transaction_repository.get_data()

    # Load mail configuration
    sender_email = os.environ.get("SENDER_EMAIL")
    sender_password = os.environ.get("SENDER_PASSWORD")
    smtp_host = os.environ.get("SMTP_HOST_SERVER")
    smtp_port = os.environ.get("SMTP_PORT")

    # Create email sender object
    email_sender = SmtpEmailSender(smtp_host, smtp_port, sender_email, sender_password, logger)

    # Create transaction service object
    transaction_service = TransactionService(transaction_repository, email_sender, logger)

    # Generate transactions report
    report = transaction_service.generate_data_report()

    # Load recipient list
    receivers_list = load_recipient("data/recipient/recipient_emails.csv")

    # Send transactions report
    transaction_service.send_transactions_report(report, receivers_list)
