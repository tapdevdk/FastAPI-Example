import logging
import os
from fastapi import APIRouter, HTTPException
import psycopg2

from app.settings import Settings

settings = Settings()
router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/")
async def update_admin():
    return {"message": "Admin getting busy"}

@router.get("/db/install")
async def install_db():
    conn = None
    try:
        conn = _get_db_client()
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=500, detail="Internal Server Error")
    
    try:
        db_schema_filepath = os.path.join(os.getcwd(), "schema.sql")
        cursor = conn.cursor()
        cursor.execute(open(db_schema_filepath, "r").read())
        conn.commit()
        conn.close()
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=500, detail="Internal Server Error")

    return {"message": "Success!"}


# PRIVATE stuff
def _get_db_client():
    return psycopg2.connect(f"host='{settings.db_host}' dbname='{settings.db_name}' user='{settings.db_username}' password='{settings.db_password}'")
