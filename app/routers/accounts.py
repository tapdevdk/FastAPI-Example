from fastapi import APIRouter

router = APIRouter()


@router.get("/accounts/", tags=["accounts"])
async def read_users():
    return [{"username": "Rick"}, {"username": "Morty"}]


@router.get("/accounts/me", tags=["accounts"])
async def read_user_me():
    return {"username": "fakecurrentuser"}


@router.get("/accounts/{username}", tags=["accounts"])
async def read_user(username: str):
    return {"username": username}
