
import logging
from app.repositories.blog.models import Blog
from app.utils import db_get_client

logger = logging.getLogger(__name__)

TABLE_NAME = "blogs"
KWARG_DB_CONNECTION = "conn"

def get_all(**kwargs):
    conn = kwargs.get(KWARG_DB_CONNECTION, db_get_client())
    
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM blogs ORDER BY created DESC")
    rows = cursor.fetchall()

    return [_map_db_row_to_blog(row) for row in rows]

def get_by_id(id: str, **kwargs):
    return _get_by_field("id", id, **kwargs)

def get_by_title(username: str, **kwargs):
    return _get_by_field("title", username, **kwargs)

def create(blog: Blog, **kwargs) -> Blog:
    conn = kwargs.get(KWARG_DB_CONNECTION, db_get_client())
    cursor = conn.cursor()

    cursor.execute(f"INSERT INTO {TABLE_NAME} (title, body, created_by) VALUES (%s, %s, %s)", (
        blog.title,
        blog.body,
        blog.created_by
    ))
    conn.commit()

    # cleanup
    cursor.close()
    if KWARG_DB_CONNECTION not in kwargs:
        conn.close()

    # Return the newly created user
    return _get_by_field("title", blog.title, **kwargs)

def update(id: str, updated_blog: Blog, **kwargs) -> Blog:
    conn = kwargs.get("conn", db_get_client())
    cursor = conn.cursor()

    sql_set = ", ".join([f"{k} = %s" for k in updated_blog.__dict__.keys() if getattr(updated_blog, k)])
    values_tuple = tuple(v for v in updated_blog.__dict__.values() if v)
    cursor.execute(f"UPDATE {TABLE_NAME} SET {sql_set}, updated = NOW() WHERE id = %s", values_tuple + (id,))
    conn.commit()
    
    # cleanup
    cursor.close()
    if KWARG_DB_CONNECTION not in kwargs:
        conn.close()

    return get_by_id(id, **kwargs)

# PRIVATE methods

def _get_by_field(field: str, value: str, **kwargs):
    conn = kwargs.get("conn", db_get_client())
    cursor = conn.cursor()

    cursor.execute(f"SELECT * FROM {TABLE_NAME} WHERE {field} = %s ORDER BY created DESC", (value,))

    row = cursor.fetchone()
    cursor.close()

    if KWARG_DB_CONNECTION not in kwargs:
        conn.close()
    
    return _map_db_row_to_blog(row)

def _map_db_row_to_blog(row: tuple) -> Blog | None:
    if not row:
        return row

    return Blog(
        id=row['id'],
        title=row['title'],
        body=row['body'],
        created=row['created'],
        created_by=row['created_by'],
        updated=row['updated'],
    )