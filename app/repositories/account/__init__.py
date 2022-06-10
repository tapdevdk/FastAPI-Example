from app.repositories.account.models import Account
from app.utils import db_get_client

def get_by_id(id: str, **kwargs):
    return _get_by_field("id", id, **kwargs)

def get_by_username(username: str, **kwargs):
    return _get_by_field("username", username, **kwargs)

def _get_by_field(field: str, value: str, **kwargs):
    conn = kwargs.get("conn", db_get_client())
    cursor = conn.cursor()

    cursor.execute(f"SELECT * FROM accounts WHERE {field} = %s", (value,))

    row = cursor.fetchone()

    cursor.close()
    conn.close()
    
    return Account(
        id=row['id'],
        username=row['username'],
        email=row['email'],
        created=row['created'],
        updated=row['updated'],
    )