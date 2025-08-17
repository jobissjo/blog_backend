import msgspec
from datetime import datetime


class CommentBase(msgspec.Struct):
    content: str


class CommentCreate(CommentBase):
    post_id: int


class CommentUpdate(msgspec.Struct):
    content: str


class CommentRead(CommentBase):
    id: int
    user_id: int
    post_id: int
    created_at: datetime
    updated_at: datetime | None = None
