from fastapi import APIRouter, Depends, HTTPException

from ..dependencies import get_token_header

router = APIRouter(
    prefix="/blogs",
    tags=["blogs"],
    dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)


fake_blogs_db = {
    "some-test-blog-uuid-1": {
        "title": "A fancy blog test title",
        "created": "2022-01-01 08:00:00Z",
        "created_by": "some-test-account-uuid-1",
        "body": "Mollit magna qui irure quis consequat. Ex tempor reprehenderit laborum pariatur minim labore esse aliqua. " +
                "Pariatur tempor cupidatat esse aliquip do nulla magna ad dolor. Dolore est id anim non ea sint voluptate labore. Cupidatat nostrud in id dolor proident."
    },
    "some-test-blog-uuid-2": {
        "title": "Another fancy blog test title",
        "created": "2022-01-01 09:00:00Z",
        "created_by": "some-test-account-uuid-1",
        "body": "A second fancy blog.. with little content"
    }
}


@router.get("/")
async def read_blogs():
    return fake_blogs_db


@router.get("/{blog_id}")
async def read_blog(blog_id: str):
    if blog_id not in fake_blogs_db:
        raise HTTPException(status_code=404, detail="Item not found")

    return fake_blogs_db[blog_id]


@router.put("/{blog_id}", tags=["custom"], responses={403: {"description": "Operation forbidden"}},)
async def update_item(blog_id: str):
    if blog_id != "some-test-blog-uuid-1":
        raise HTTPException(
            status_code=403, detail="You can only update the item: plumbus"
        )

    return {"blog_id": blog_id, "name": "The great Plumbus"}
