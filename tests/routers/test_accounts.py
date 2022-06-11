from fastapi.testclient import TestClient
from app.main import app
from app.repositories.account.models import Account

from tests.utils import get_test_account

client = TestClient(app)

APP_TOKEN = "magenta"
APP_HEADER_X_TOKEN = "fake-super-secret-magenta-token"

def test_read_accounts(mocker):
    test_accounts = [get_test_account()]
    mocker.patch(
        'app.routers.accounts.get_all',
        return_value=test_accounts
    )

    response = client.get(f"/accounts?token={APP_TOKEN}", headers={"X-Token": APP_HEADER_X_TOKEN})
    response_accounts = [Account(**element) for element in response.json()]
    
    assert response.status_code == 200
    assert response_accounts == test_accounts

def test_read_accounts_me(mocker):
    test_account = get_test_account()
    mocker.patch(
        'app.routers.accounts.get_by_auth_token',
        return_value=test_account
    )

    response = client.get(f"/accounts/me?token={APP_TOKEN}", headers={"X-Token": APP_HEADER_X_TOKEN})
    response_account = Account(**response.json())

    assert response.status_code == 200
    assert response_account == test_account