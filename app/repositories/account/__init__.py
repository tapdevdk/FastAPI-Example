from app.repositories.account.models import Account
from app.utils import db_get_client

TABLE_NAME = "accounts"
KWARG_DB_CONNECTION = "conn"

def get_all(**kwargs):
    conn = kwargs.get(KWARG_DB_CONNECTION, db_get_client())
    
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM {TABLE_NAME} ORDER BY created DESC")
    rows = cursor.fetchall()

    cursor.close()
    if KWARG_DB_CONNECTION not in kwargs:
        conn.close()

    return [_map_row_to_account(row) for row in rows]

def get_by_id(id: str, **kwargs):
    return _get_by_field("id", id, **kwargs)

def get_by_username(username: str, **kwargs):
    return _get_by_field("username", username, **kwargs)

# def get_authenticated_account(account: Account, **kwargs):
def get_authenticated_account(username: str, password: str, **kwargs):
    conn = kwargs.get("conn", db_get_client())
    cursor = conn.cursor()

    cursor.execute(f"SELECT * FROM {TABLE_NAME} WHERE username = %s AND password = crypt(%s, password)", (
        username, password
    ))

    row = cursor.fetchone()

    cursor.close()
    if KWARG_DB_CONNECTION not in kwargs:
        conn.close()
    
    return _map_row_to_account(row)

def get_by_auth_token(auth_token: str) -> Account:
    # HACK: The app has no proper authentication. This should be removed
    return get_by_username("test")

# PRIVATE methods

def _get_by_field(field: str, value: str, **kwargs):
    conn = kwargs.get("conn", db_get_client())
    cursor = conn.cursor()

    cursor.execute(f"SELECT * FROM {TABLE_NAME} WHERE {field} = %s", (value,))

    row = cursor.fetchone()

    cursor.close()
    if KWARG_DB_CONNECTION not in kwargs:
        conn.close()
    
    return _map_row_to_account(row)

def _map_row_to_account(row) -> Account | None:
    if row is None:
        return None

    return Account(
        id=row['id'],
        username=row['username'],
        email=row['email'],
        created=row['created'],
        updated=row['updated'],
    )