# app/domain/posts/repository.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update

from app.core.exceptions import AppException
from .models import Post, Tag
from .schema import BlogPostUpdate, BlogPostCreate
from sqlalchemy.orm import selectinload


class PostRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all(self):
        result = await self.session.execute(select(Post).options(selectinload(Post.tags)))
        return result.scalars().all()
    
    async def get_user_posts(self, user_id: int):
        result = await self.session.execute(
            select(Post).where(Post.author_id == user_id).options(selectinload(Post.tags),selectinload(Post.author)  )
        )
        return result.scalars().all()

    async def get_by_id(self, post_id: int) -> Post | None:

        result = await self.session.execute(select(Post).where(Post.id == post_id).options(selectinload(Post.tags),selectinload(Post.author) ))
        return result.scalar_one_or_none()

    async def add(self, post: Post):
        print("In repo", post)
        self.session.add(post)
        await self.session.commit()
        await self.session.refresh(post, attribute_names=["tags"])
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

        stmt = update(Post).where(Post.id == post_id).values(**data).returning(Post)

        result = await self.session.execute(stmt)
        await self.session.commit()

        return result.scalar_one_or_none()

    async def get_or_create_tags(self, tag_names: list[str]) -> list[Tag]:
        tags = []
        for tag_name in tag_names:
            tag = await self.session.execute(select(Tag).where(Tag.name == tag_name))
            tag = tag.scalar_one_or_none()
            if tag:
                tags.append(tag)
            else:
                new_tag = Tag(name=tag_name)
                self.session.add(new_tag)
                await self.session.commit()
                tags.append(new_tag)
        return tags
