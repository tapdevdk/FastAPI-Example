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

def _map_row_to_account(row):
    return Account(
        id=row['id'],
        username=row['username'],
        email=row['email'],
        created=row['created'],
        updated=row['updated'],
    )