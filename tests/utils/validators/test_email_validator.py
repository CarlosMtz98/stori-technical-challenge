import pytest

from app.utils.validators.validate_email import is_valid_email

# Valid email addresses
valid_emails = [
    "example.email@domain.com",
    "test-email@example.co.uk",
    "my.email@sub-domain.some.tld",
]

# Invalid email addresses
invalid_emails = [
    "not_an_email",
    "email@.com",
    "@domain.com",
    "email@.com",
    "email@domain.c",
    "email@domain.c.",
    "email@domain.c!",
]


@pytest.mark.parametrize("email", valid_emails)
def test_valid_email(email):
    assert is_valid_email(email)


@pytest.mark.parametrize("email", invalid_emails)
def test_invalid_email(email):
    assert is_valid_email(email) == False
