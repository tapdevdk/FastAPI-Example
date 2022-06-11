from datetime import datetime
from app.repositories.account.models import Account


def get_test_account(**kwargs):
    return Account(
            id=kwargs.get("id", "test-id"),
            username=kwargs.get("username", "testtest"),
            password=kwargs.get("password", "ainsecuretestpwd"),
            email=kwargs.get("email", "test@testtest.dk"),
            created=kwargs.get("created", datetime.utcnow()),
            updated=kwargs.get("updated", datetime.utcnow()),
        )