from unittest.mock import MagicMock, patch
from fastapi.testclient import TestClient
from app.main import app
from app.repositories.account.models import Account

from tests.utils import get_test_account

client = TestClient(app)

APP_TOKEN = "magenta"
APP_HEADER_X_TOKEN = "fake-super-secret-magenta-token"

@patch('app.routers.accounts.get_all')
def test_read_accounts(mocked_get_all: MagicMock):
    test_accounts = [get_test_account()]
    mocked_get_all.return_value = test_accounts

    response = client.get(f"/accounts?token={APP_TOKEN}", headers={"X-Token": APP_HEADER_X_TOKEN})
    response_accounts = [Account(**element) for element in response.json()]
    
    mocked_get_all.assert_called_once()
    assert response.status_code == 200
    assert response_accounts == test_accounts

@patch('app.routers.accounts.get_by_auth_token')
def test_read_accounts_me(mocked_get_by_auth_token: MagicMock):
    test_acc = get_test_account()
    mocked_get_by_auth_token.return_value = test_acc
    response = client.get(f"/accounts/me?token={APP_TOKEN}", headers={"X-Token": APP_HEADER_X_TOKEN})

    assert response.status_code == 200
    mocked_get_by_auth_token.assert_called_once_with(APP_HEADER_X_TOKEN)

@patch('app.routers.accounts.get_by_username')
def test_read_account_by_username(mocked_get_by_username: MagicMock):
    test_acc = get_test_account()
    mocked_get_by_username.return_value = test_acc
    response = client.get(f"/accounts/{test_acc.username}?token={APP_TOKEN}", headers={"X-Token": APP_HEADER_X_TOKEN})

    assert response.status_code == 200
    mocked_get_by_username.assert_called_once_with(test_acc.username)

@patch('app.routers.accounts.get_authenticated_account')
def test_auth_account(mocked_get_authenticated_account: MagicMock):
    test_acc = get_test_account()
    mocked_get_authenticated_account.return_value = test_acc
    response = client.post(f"/accounts/authenticate?token={APP_TOKEN}", headers={"X-Token": APP_HEADER_X_TOKEN}, json={
        "username": test_acc.username,
        "password": test_acc.password
    })

    assert response.status_code == 200
    mocked_get_authenticated_account.assert_called_once_with(test_acc.username, test_acc.password)