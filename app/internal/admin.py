import logging
import os
from fastapi import APIRouter, HTTPException

from app.settings import Settings
from app.utils import db_get_client

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
        conn = db_get_client()
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
