from fastapi import Depends, FastAPI

from .dependencies import get_query_token, get_token_header
from .internal import admin
from .routers import accounts, blogs

app = FastAPI(dependencies=[Depends(get_query_token)])

# Admin router
app.include_router(admin.router, prefix="/admin", tags=["admin"],
    dependencies=[Depends(get_token_header)],
    responses={418: {"description": "I'm a teapot"}},
)

# Other routers
app.include_router(accounts.router)
app.include_router(blogs.router)

# Root path
@app.get("/")
async def root():
    return {"message": "Welcome to TapDev's FastAPI Example!"}