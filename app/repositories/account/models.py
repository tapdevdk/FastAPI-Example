from typing import Optional
from pydantic import BaseModel
from datetime import datetime


class Account(BaseModel):
    id: Optional[str]
    username: str
    password: Optional[str]
    email: Optional[str]
    created: Optional[datetime]
    updated: Optional[datetime]