from datetime import datetime
from app.repositories.account.models import Account


def get_test_account(**kwargs):
    return Account(
            id=kwargs.get("id", "test-id"),
            username=kwargs.get("username", "testtest"),
            email=kwargs.get("email", "test@testtest.dk"),
            created=kwargs.get("created", datetime.utcnow()),
            updated=kwargs.get("updated", datetime.utcnow()),
        )