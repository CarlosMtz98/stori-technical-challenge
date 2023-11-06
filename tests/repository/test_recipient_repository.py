import pytest
from unittest.mock import Mock, patch
from app.models.recipient import Recipient
from app.repository.recipient_repository import RecipientRepository

@pytest.fixture
def mock_session():
    mock = Mock()
    mock.query.return_value = mock
    return mock

@pytest.fixture
def recipient_repository(mock_session):
    return RecipientRepository(mock_session)


def test_create_valid_recipient(mock_session, recipient_repository):
    recipient = Recipient(id=1, email="test@example.com", first_name="Dennis", last_name="Ritchie")
    recipient_repository.get_by_email = Mock(return_value=None)
    recipient_repository.create(recipient)

    mock_session.add.assert_called_once_with(recipient)
    mock_session.commit.assert_called_once()


def test_create_invalid_email(mock_session, recipient_repository):
    recipient = Recipient(id=1, email="test@example", first_name="Dennis", last_name="Ritchie")
    recipient_repository.create(recipient)
    mock_session.add.assert_not_called()
    mock_session.commit.assert_not_called()


def test_create_email_already_exists(mock_session, recipient_repository):
    recipient = Recipient(id=1, email="test@example", first_name="Dennis", last_name="Ritchie")
    recipient_repository.get_by_email = Mock(return_value=Recipient)
    recipient_repository.create(recipient)
    mock_session.add.assert_not_called()
    mock_session.commit.assert_not_called()


def test_get_all(mock_session, recipient_repository):
    recipients = [
        Recipient(id=1, email="test1@example.com", first_name="Dennis", last_name="Ritchie"),
        Recipient(id=2, email="test2@example.com", first_name="Richard", last_name="Stallman")
    ]
    mock_session.query(Recipient).all.return_value = recipients
    result = recipient_repository.get_all()
    assert result == recipients


def test_get_by_id_exists(mock_session, recipient_repository):
    recipient = Recipient(id=1, email="test1@example.com", first_name="Dennis", last_name="Ritchie")
    recipient_id = 1
    mock_session.query(Recipient).get.return_value.return_value = recipient
    result = recipient_repository.get_by_id(recipient_id)
    assert result is not None


def test_get_by_id_not_found(mock_session, recipient_repository):
    recipient_id = 1
    mock_session.query(Recipient).get.return_value = None
    result = recipient_repository.get_by_id(recipient_id)
    assert result is None


def test_update(mock_session, recipient_repository):
    recipient = Recipient(id=2, email="test2@example.com", first_name="Richard", last_name="Stallman")
    recipient_repository.update(recipient)
    mock_session.merge.assert_called_once_with(recipient)
    mock_session.commit.assert_called_once()


def test_delete_exists(mock_session, recipient_repository):
    recipient = Recipient(id=1, email="test2@example.com", first_name="Richard", last_name="Stallman")
    recipient_id = 1
    recipient_repository.get_by_id = Mock(return_value=recipient)
    recipient_repository.delete(recipient_id)
    mock_session.delete.assert_called_once()
    mock_session.commit.assert_called_once()


def test_delete_not_found(mock_session, recipient_repository):
    recipient_id = 1
    recipient_repository.get_by_id = Mock(return_value=None)
    recipient_repository.delete(recipient_id)
    mock_session.delete.assert_not_called()
    mock_session.commit.assert_not_called()

