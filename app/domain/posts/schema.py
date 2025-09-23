from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict
from dataclasses import dataclass, field
from app.domain.posts.models import Tag
from app.domain.users.schemas import UserBasicSchema
from litestar.datastructures import UploadFile


@dataclass
class BlogPostCreateForm:
    title: str
    content: str
    excerpt: str
    image: Optional[UploadFile]  = None
    series_id: Optional[int] = None
    tags: Optional[List[str]] = field(default_factory=list)


# Base schema for shared fields
class BlogPostBase(BaseModel):
    title: str
    content: str
    excerpt: str
    tags: Optional[List[str]] = []


# Schema for creating a new blog post
class BlogPostCreate(BlogPostBase):
    pass


# Schema for updating a blog post
class BlogPostUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    excerpt: Optional[str] = None
    image_url: Optional[str] = None
    tags: Optional[List[int]] = None

    model_config = ConfigDict(from_attributes=True)

class BlogTagRead(BaseModel):
    id: int
    name: str

    model_config = ConfigDict(from_attributes=True)

# Schema for reading a blog post
class BlogPostRead(BaseModel):
    id: int
    title: str
    content: str
    created_at: datetime = Field(alias='createdAt', default=None)
    excerpt: str
    updated_at: Optional[datetime] = Field(alias='updatedAt', default=None)
    tags: Optional[List[BlogTagRead]]   
    image_url: Optional[str] = None
    author_id: int
    author: Optional[UserBasicSchema] = None

    model_config = ConfigDict(from_attributes=True)
