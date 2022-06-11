import logging
from fastapi import APIRouter, Depends, HTTPException, Header
from app.repositories.account import get_by_auth_token, get_by_username
from app.repositories.blog import create, get_all, get_by_id, update
from app.repositories.blog.models import Blog

from ..dependencies import get_token_header


logger = logging.getLogger(__name__)
router = APIRouter(
    prefix="/blogs",
    tags=["blogs"],
    dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)

@router.get("/")
async def read_blogs():
    try:
        return get_all()
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.get("/{blog_id}")
async def read_blog(blog_id: str):
    try:
        return get_by_id(blog_id)
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.post("/")
async def create_blog(new_blog: Blog, x_token: str = Header()):
    try:
        created_by_acc = get_by_auth_token(x_token)
        new_blog.created_by = created_by_acc.id
        return create(new_blog)
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.post("/{blog_id}")
async def update_item(blog_id: str, updated_blog: Blog):
    try:
        return update(blog_id, updated_blog)
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=500, detail="Internal Server Error")
