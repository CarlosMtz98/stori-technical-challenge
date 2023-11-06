from datetime import datetime

from sqlalchemy import Column, Integer, DateTime, Numeric, Uuid, MetaData, Enum, Float, String
from sqlalchemy.orm import registry
from sqlalchemy.testing.schema import Table

from app.models.recipient import Recipient
from app.models.transaction import Transaction, TransactionType

now = datetime.utcnow
metadata = MetaData()
mapper_registry = registry(metadata=metadata)

transaction_table = Table(
    'transaction',
    mapper_registry.metadata,
    Column('id', Integer, autoincrement=True, primary_key=True),
    Column('datetime', DateTime, default=now),
    Column('amount', Float, nullable=False),
    Column('type', Enum(TransactionType), nullable=False),
    Column('idempotency_id', Uuid)
)

recipient_table = Table(
    'recipient',
    mapper_registry.metadata,
    Column('id', Integer, autoincrement=True, primary_key=True),
    Column('email', String(255), unique=True, nullable=False),
    Column('first_name', String(255)),
    Column('last_name', String(255))
)


def start_mapping():
    mapper_registry.map_imperatively(Transaction, transaction_table)
    mapper_registry.map_imperatively(Recipient, recipient_table)

