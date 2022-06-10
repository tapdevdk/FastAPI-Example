import logging
from fastapi import APIRouter, HTTPException
from app.repositories.account import get_all, get_by_username
from app.utils import account_get_by_username

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/accounts/", tags=["accounts"])
async def read_accounts():
    try:
        return get_all()
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.get("/accounts/me", tags=["accounts"])
async def read_accounts_me():
    try:
        return get_by_username("test") # HACK: The app has no proper authentication. This should be removed
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
