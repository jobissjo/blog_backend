# app/domain/posts/repository.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update

from app.core.exceptions import AppException
from .models import Post
from .schema import BlogPostUpdate, BlogPostCreate

class PostRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def  get_all(self):
        result = await self.session.execute(select(Post))
        return result.scalars().all()

    async def get_by_id(self, post_id: int) -> Post | None:
        print("In repo get by id", post_id)
        result = await self.session.execute(select(Post).where(Post.id == post_id))
        return result.scalar_one_or_none()

    async def add(self, post: Post):
        self.session.add(post)
        await self.session.commit()
        return post

    async def update(self, post: Post, post_data: BlogPostUpdate):
        # Convert Pydantic model to dict
        data = post_data.model_dump(exclude_unset=True)
        print("In repo", data)

        for key, value in data.items():
            setattr(post, key, value)
        await self.session.commit()
        return post
    
    async def delete(self, post_id: int):
        post = await self.get_by_id(post_id)
        if not post:
            raise AppException("Post not found", status_code=404)
        await self.session.delete(post)
        await self.session.commit()

    async def update_by_id(self, post_id: int, post_data: BlogPostCreate):
        # Convert Pydantic model to dict
        data = post_data.model_dump()

        stmt = (
            update(Post)
            .where(Post.id == post_id)
            .values(**data)
            .returning(Post)
        )

        result = await self.session.execute(stmt)
        await self.session.commit()

        return result.scalar_one_or_none()