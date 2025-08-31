from datetime import datetime
from pydantic import BaseModel


class CommentBase(BaseModel):
    content: str

    class Config:
        from_attributes = True


class CommentCreate(CommentBase):
    post_id: int


class CommentUpdate(BaseModel):
    content: str

    class Config:
        from_attributes = True


class CommentRead(CommentBase):
    id: int
    user_id: int
    post_id: int
    created_at: datetime
    updated_at: datetime | None = None

    class Config:
        from_attributes = True
