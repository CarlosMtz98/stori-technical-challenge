import logging

import pytest
import smtplib
from unittest.mock import MagicMock, patch
from app.utils.email.smtp_email_sender import SmtpEmailSender


@pytest.fixture
def mock_smtp():
    smtp = MagicMock(spec=smtplib.SMTP)
    return smtp


@pytest.fixture
def smtp_email_sender(mock_smtp, caplog):
    logger = logging.getLogger("custom_logger")
    logger.addHandler(caplog.handler)
    sender = SmtpEmailSender(
        host="smtp.example.com",
        port=465,
        sender_email="test@example.com",
        sender_password="password",
        logger=logger,
    )
    sender.server = mock_smtp
    return sender


def test_load_template_success():
    sender = SmtpEmailSender("host", 465, "email", "password", None)
    template_file = "example_template.txt"
    expected_content = "Template content"
    with patch("builtins.open", create=True) as mock_open:
        mock_open.return_value.__enter__().read.return_value = expected_content
        result = sender.load_template(template_file)
        assert result == expected_content


def test_load_template_file_not_found(caplog):
    sender = SmtpEmailSender("host", 465, "email", "password", None)
    template_file = "non_existent_template.txt"
    sender.load_template(template_file)
    assert "File not found" in caplog.text


def test_load_template_exception(caplog):
    sender = SmtpEmailSender("host", 465, "email", "password", None)
    template_file = "example_template.txt"
    with patch("builtins.open", create=True) as mock_open:
        mock_open.return_value.__enter__().read.side_effect = Exception("Mocked exception")
        sender.load_template(template_file)
        assert "Mocked exception" in caplog.text


def test_render_template_exception(smtp_email_sender, caplog):
    template_file = "example_template.txt"
    params = {"key": "value"}
    with patch("jinja2.Environment.from_string", side_effect=Exception("Mocked exception")):
        smtp_email_sender.render_template(template_file, params)
        assert "Mocked exception" in caplog.text


def test_send_email_no_server(smtp_email_sender, caplog):
    smtp_email_sender.server = None
    smtp_email_sender.send_email("recipient@example.com", "Test Subject", "<p>Test content</p>")
    for record in caplog.records:
        assert record.levelname == "ERROR"
