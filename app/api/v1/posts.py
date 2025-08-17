from litestar import Controller, get, post, delete, put
from app.domain.posts.service import PostService
from app.domain.posts.repository import PostRepository
from sqlalchemy.ext.asyncio import AsyncSession
from app.domain.posts.schema import BlogPostRead, BlogPostCreate


class PostController(Controller):
    path = "api/v1/posts"
    tags = ["Posts"]

    @get("/")
    async def list_posts(self, session: AsyncSession)-> list[BlogPostRead]:
        service = PostService(PostRepository(session))
        return await service.list_posts()

    @post("/")
    async def create_post(self, data: BlogPostCreate, session: AsyncSession) -> BlogPostRead:
        service = PostService(PostRepository(session))
        return await service.create_post(data)

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
    async def update_post(self, post_id: int, data: BlogPostCreate, session: AsyncSession) -> BlogPostRead:
        service = PostService(PostRepository(session))
        return await service.update_post(post_id, data)
    
    

