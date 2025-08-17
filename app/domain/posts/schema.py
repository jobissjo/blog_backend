import msgspec
from typing import List, Optional
from datetime import datetime


# Base schema for shared fields
class BlogPostBase(msgspec.Struct):
    title: str
    content: str
    excerpt: str
    author: str
    tags: List[str]
    image_url: Optional[str] = None


# Schema for creating a new blog post
class BlogPostCreate(BlogPostBase):
    pass


# Schema for updating a blog post
class BlogPostUpdate(msgspec.Struct, omit_defaults=True):  
    # omit_defaults=True makes fields optional for partial updates
    title: Optional[str] = None
    content: Optional[str] = None
    excerpt: Optional[str] = None
    author: Optional[str] = None
    tags: Optional[List[str]] = None
    image_url: Optional[str] = None


# Schema for reading a blog post
class BlogPostRead(msgspec.Struct):
    id: int
    title: str
    content: str
    excerpt: str
    author: str
    tags: List[str]
    created_at: datetime
    updated_at: datetime
    image_url: Optional[str] = None
