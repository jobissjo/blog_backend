from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel


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

    class Config:
        from_attributes = True


# Schema for reading a blog post
class BlogPostRead(BaseModel):
    id: int
    title: str
    content: str
    excerpt: str
    created_at: datetime
    updated_at: datetime
    tags: Optional[List[str]] = []
    image_url: Optional[str] = None

    class Config:
        from_attributes = True
