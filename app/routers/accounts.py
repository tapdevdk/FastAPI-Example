import logging
from fastapi import APIRouter, HTTPException
from app.repositories.account import get_by_username
from app.utils import account_get_by_username, db_get_client

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/accounts/", tags=["accounts"])
async def read_accounts():
    conn = None
    try:
        conn = db_get_client()
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=500, detail="Internal Server Error")
    
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM accounts ORDER BY username ASC")
        rows = cursor.fetchall()

        return [{
            "id": row["id"],
            "username": row["username"],
            "email": row["email"],
        } for row in rows]
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.get("/accounts/me", tags=["accounts"])
async def read_accounts_me():
    # TODO: We have no proper authentication yet, so this is a HACK and should be removed.
    try:
        return get_by_username("test")
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.get("/accounts/{username}", tags=["accounts"])
async def read_user(username: str):
    try:
        acc = account_get_by_username(username)
        if not acc:
            raise HTTPException(status_code=404, detail="Not found")

        return acc
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=500, detail="Internal Server Error")
