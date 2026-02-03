from pydantic import BaseModel
from datetime import datetime
from app.schemas.user import UserRead

class PostCreate(BaseModel):
    title: str
    content: str

class PostRead(BaseModel):
    id: int
    title: str
    content: str
    author: UserRead
    created_at: datetime

    class Config:
        from_attributes = True
