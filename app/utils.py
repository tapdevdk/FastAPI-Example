import logging
import psycopg2
from psycopg2.extras import RealDictCursor
from app.settings import Settings

logger = logging.getLogger(__name__)
settings = Settings()

def db_get_client():
    return psycopg2.connect(f"host='{settings.db_host}' dbname='{settings.db_name}' user='{settings.db_username}' password='{settings.db_password}'", 
        cursor_factory=RealDictCursor)