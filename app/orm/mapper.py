from datetime import datetime

from sqlalchemy import Column, Integer, DateTime, Numeric, Uuid, MetaData, Enum, Float
from sqlalchemy.orm import registry
from sqlalchemy.testing.schema import Table

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
    Column('idempotencyid', Uuid)
)


def start_mapping():
    mapper_registry.map_imperatively(Transaction, transaction_table)

