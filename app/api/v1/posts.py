from litestar import Controller, get, post, delete, put
from app.domain.posts.service import PostService
from app.domain.posts.repository import PostRepository
from sqlalchemy.ext.asyncio import AsyncSession
from app.domain.posts.schema import BlogPostCreateForm, BlogPostRead, BlogPostCreate
from litestar.connection import Request
from typing import Annotated
from litestar.params import Body
from litestar.enums import RequestEncodingType


class PostController(Controller):
    path = "api/v1/posts"
    tags = ["Posts"]

    @get("/")
    async def list_posts(self, session: AsyncSession)-> list[BlogPostRead]:
        service = PostService(PostRepository(session))
        return await service.list_posts()

    @post("/")
    async def create_post(self, request: Request, data: Annotated[BlogPostCreateForm, Body(media_type=RequestEncodingType.MULTI_PART)], session: AsyncSession) -> BlogPostRead:
        service = PostService(PostRepository(session))
        return await service.create_post(data, request.user.id)

    @get("/{post_id:int}")
    async def get_post(self, post_id: int, session: AsyncSession) -> BlogPostRead:
        service = PostService(PostRepository(session))
        return await service.get_post(post_id)
    
    @delete("/{post_id:int}")
    async def delete_post(self, post_id: int, session: AsyncSession) -> None:
        service = PostService(PostRepository(session))
        await service.delete_post(post_id)
        return None
    
    @put("/{post_id:int}")
    async def update_post(self, post_id: int, data: Annotated[BlogPostCreateForm, Body(media_type=RequestEncodingType.MULTI_PART)], session: AsyncSession) -> BlogPostRead:
        service = PostService(PostRepository(session))
        return await service.update_post(post_id, data)
    
    @get("/user-posts")
    async def list_user_posts(self, request: Request, session: AsyncSession) -> list[BlogPostRead]:
        service = PostService(PostRepository(session))
        return await service.list_user_posts(request.user.id)
    
    

