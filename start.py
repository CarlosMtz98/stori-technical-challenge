from sqlalchemy.orm import sessionmaker

import app.config.logging_config
import os
import logging

from sqlalchemy import create_engine

from app.orm.mapper import start_mapping
from app.repository.recipient_repository import RecipientRepository
from app.repository.transaction_repository import TransactionRepository
from app.services.transaction_service import TransactionService
from dotenv import load_dotenv

from app.utils.email.smtp_email_sender import SmtpEmailSender
from app.utils.file_reader.csv_file_reader import CSVFileReader


def load_recipient(file_location):
    recipient_list = set()
    reader = CSVFileReader(file_location)
    data = reader.read_csv_as_dict()
    for item in data:
        recipient_list.add(item.get("email"))

    return recipient_list


if __name__ == "__main__":
    load_dotenv()
    logger = logging.getLogger('app')

    # ConnectIo to the database
    db_user = os.environ.get("POSTGRES_USER")
    db_password = os.environ.get("POSTGRES_PASSWORD")
    db_host = os.environ.get("DB_HOST") if os.environ.get("DB_HOST") else "127.0.0.1"
    db_port = os.environ.get("DB_PORT")
    db_name = os.environ.get("POSTGRES_DB")
    db_connection_string = f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'
    db_engine = create_engine(db_connection_string)

    start_mapping()
    db_session = sessionmaker(bind=db_engine)
    session = db_session()

    # Create transaction repository object
    transactions_file_location = 'data/transactions/transactions_example.csv'
    transaction_repository = TransactionRepository(session, transactions_file_location)

    # Create recipient repository
    recipient_repository = RecipientRepository(session)

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
    receivers_list = [recipient.email for recipient in recipient_repository.get_all()]

    # Send transactions report
    transaction_service.send_transactions_report(report, receivers_list)
