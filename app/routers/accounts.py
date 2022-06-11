import logging
from typing import Union
from fastapi import APIRouter, Depends, HTTPException, Header
from app.dependencies import get_token_header
from app.repositories.account import get_all, get_authenticated_account, get_by_auth_token, get_by_username
from app.repositories.account.models import Account

logger = logging.getLogger(__name__)
router = APIRouter(
    prefix="/accounts",
    tags=["accounts"],
    dependencies=[Depends(get_token_header)],
)


@router.get("/")
async def read_accounts():
    try:
        return get_all()
    except Exception as e:
        logger.exception(e)
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.get("/me")
async def read_accounts_me(x_token: Union[str, None] = Header(default=None)):
    try:
        return get_by_auth_token(x_token).dict(exclude_none=True) # HACK: The app has no proper authentication. This should be removed
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
async def auth_account(account: Account):
    try:
        acc = get_authenticated_account(account.username, account.password)
        if not acc:
            raise HTTPException(status_code=401, detail="Unauthorized")

        return acc.dict(exclude_none=True)
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.exception(e)
        raise HTTPException(status_code=500, detail="Internal Server Error")