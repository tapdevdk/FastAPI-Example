import logging
from fastapi import APIRouter, HTTPException
from app.repositories.account import get_all, get_authenticated_account, get_by_username
from app.repositories.account.models import Account

logger = logging.getLogger(__name__)
router = APIRouter(
    prefix="/accounts",
    tags=["accounts"],
)


@router.get("/")
async def read_accounts():
    try:
        return get_all()
    except Exception as e:
        logger.exception(e)
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.get("/me")
async def read_accounts_me():
    try:
        return get_by_username("test").dict(exclude_none=True) # HACK: The app has no proper authentication. This should be removed
    except Exception as e:
        logger.exception(e)
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.get("/{username}")
async def read_user(username: str):
    try:
        acc = get_by_username(username)
        if not acc:
            raise HTTPException(status_code=404, detail="Not found")

        return acc.dict(exclude_none=True)
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.exception(e)
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.post("/authenticate")
async def read_accounts(account: Account):
    try:
        acc = get_authenticated_account(account)
        if not acc:
            raise HTTPException(status_code=401, detail="Unauthorized")

        return acc.dict(exclude_none=True)
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.exception(e)
        raise HTTPException(status_code=500, detail="Internal Server Error")