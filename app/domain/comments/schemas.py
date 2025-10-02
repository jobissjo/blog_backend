from datetime import datetime
from pydantic import BaseModel, ConfigDict

from typing import Optional
from app.domain.users.schemas import UserBasicSchema

class CommentBase(BaseModel):
    content: str

    model_config = ConfigDict(from_attributes=True)


class CommentCreate(CommentBase):
    post_id: int


class CommentUpdate(BaseModel):
    content: str

    model_config = ConfigDict(from_attributes=True)


class CommentRead(CommentBase):
    id: int
    user_id: int
    post_id: int
    created_at: datetime
    updated_at: datetime | None = None
    user: Optional[UserBasicSchema] = None

    model_config = ConfigDict(from_attributes=True)
