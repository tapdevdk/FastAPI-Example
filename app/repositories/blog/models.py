from typing import Optional
from pydantic import BaseModel
from datetime import datetime


class Blog(BaseModel):
    id: Optional[str]
    title: str
    body: str
    created: Optional[datetime]
    created_by: Optional[str]
    updated: Optional[datetime]