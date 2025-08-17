# app/domain/posts/repository.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.exceptions import AppException
from .models import Post
from .schema import BlogPostUpdate, BlogPostCreate

class PostRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all(self):
        result = await self.session.execute(select(Post))
        return result.scalars().all()

    async def get_by_id(self, post_id: str):
        return await self.session.get(Post, post_id)

    async def add(self, post: Post):
        self.session.add(post)
        await self.session.commit()
        return post

    async def update(self, post_id: str, post_data: BlogPostUpdate):
        post = await self.get_by_id(post_id)

        if not post:
            raise AppException("Post not found", status_code=404)

        for key, value in post_data.dict(exclude_unset=True).items():
            setattr(post, key, value)

        self.session.add(post)
        await self.session.commit()
        return post