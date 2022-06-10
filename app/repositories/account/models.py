from pydantic import BaseModel
from datetime import datetime


class Account(BaseModel):
    id: str
    username: str
    email: str
    created: datetime
    updated: datetime