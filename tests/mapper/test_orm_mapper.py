import uuid

import pytest
from sqlalchemy import create_engine, text, select
from datetime import datetime

from app.models.recipient import Recipient
from app.orm.mapper import start_mapping, mapper_registry
from app.models.transaction import Transaction, TransactionType
from sqlalchemy.orm import sessionmaker, clear_mappers, load_only


@pytest.fixture
def in_memory_db():
    engine = create_engine("sqlite:///:memory:")
    mapper_registry.metadata.create_all(bind=engine)
    return engine


@pytest.fixture
def session(in_memory_db):
    clear_mappers()
    start_mapping()
    Session = sessionmaker(bind=in_memory_db)
    session = Session()
    yield session
    clear_mappers()


def test_transaction_mapper(session):
    idempotency_id_1 = uuid.uuid4()
    idempotency_id_2 = uuid.uuid4()

    dml = """
                INSERT INTO 'transaction'(amount, datetime, type, idempotency_id) VALUES 
                (220.00, '2023-03-19 21:57:17.525196', 'DEBIT', '{}'), 
                (32.51, '2023-10-11 10:57:17.525196', 'CREDIT', '{}')
        """.format(str(idempotency_id_1), str(idempotency_id_2))

    session.execute(text(dml))
    expected = [
        Transaction(
            1,
            datetime.strptime("2023-03-19 21:57:17.525196", "%Y-%m-%d %H:%M:%S.%f"),
            220.00,
            TransactionType.DEBIT,
            idempotency_id_1),

        Transaction(
            2,
            datetime.strptime("2023-10-11 10:57:17.525196", "%Y-%m-%d %H:%M:%S.%f"),
            32.51,
            TransactionType.CREDIT,
            idempotency_id_2)
    ]

    res = session.query(Transaction).all()

    assert res == expected


def test_transaction_add_mapper(session):
    idempotency_id_1 = uuid.uuid4()
    trx = Transaction(
            1,
            datetime.strptime("2023-03-19 21:57:17.525196", "%Y-%m-%d %H:%M:%S.%f"),
            220.00,
            TransactionType.DEBIT,
            idempotency_id_1)

    session.add(trx)
    session.commit()
    rows = list(session.query(Transaction.idempotency_id))
    assert rows == [(idempotency_id_1,)]


def test_recipient_mapper(session):
    dml = """
        INSERT INTO recipient(email, first_name, last_name) VALUES 
        ('test@domain.com', 'Greg', 'Roberts'),
        ('test2@domain.com', NULL, NULL)
    """
    session.execute(text(dml))
    expected = [
        Recipient(email='test@domain.com', id=1, first_name='Greg', last_name='Roberts'),
        Recipient(email='test2@domain.com', id=2)
    ]
    res = session.query(Recipient).all()

    assert res == expected

