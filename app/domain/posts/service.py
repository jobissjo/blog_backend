# app/domain/posts/service.py
from .repository import PostRepository
from .models import Post


class PostService:
    def __init__(self, repo: PostRepository):
        self.repo = repo

    async def list_posts(self):
        return await self.repo.get_all()

    async def get_post(self, post_id: str):
        return await self.repo.get_by_id(post_id)
    
    async def create_post(self, post: Post):
        return await self.repo.add(post)
    
    async def delete_post(self, post_id: str):
        return await self.repo.delete(post_id)
    
    async def update_post(self, post_id: str, post: Post):
        return await self.repo.update(post_id, post)
