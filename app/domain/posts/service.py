# app/domain/posts/service.py
from app.core.exceptions import AppException
from .repository import PostRepository
from .models import Post
from .schema import BlogPostCreate, BlogPostUpdate, BlogPostRead


class PostService:
    def __init__(self, repo: PostRepository):
        self.repo = repo

    async def list_posts(self)-> list[BlogPostRead]:
        return await self.repo.get_all()
         

    async def get_post(self, post_id: int):
        result = await self.repo.get_by_id(post_id)
        if not result:
            raise AppException("Post not found", status_code=404)
        return BlogPostRead.model_validate(result)

    
    async def create_post(self, post: BlogPostCreate, user_id: int) -> BlogPostRead:
        print("In service", post)
        new_post = Post(
            title=post.title,
            content=post.content,
            excerpt=post.excerpt,
            author_id=user_id
        )
        result = await self.repo.add(new_post)
        return BlogPostRead.model_validate(result)
    
    async def delete_post(self, post_id: int):
        await self.repo.delete(post_id)
    
    async def update_post(self, post_id: int, post_data: BlogPostUpdate):
        result = await self.repo.update_by_id(post_id, post_data)
        return BlogPostRead.model_validate(result) if result else None
