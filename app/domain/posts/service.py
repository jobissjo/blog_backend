# app/domain/posts/service.py
from app.core.exceptions import AppException
from app.utils.file_upload import FileUploadUtils
from .repository import PostRepository
from .models import Post
from .schema import BlogPostCreate, BlogPostCreateForm, BlogPostUpdate, BlogPostRead, BlogTagRead


class PostService:
    def __init__(self, repo: PostRepository):
        self.repo = repo

    async def list_posts(self) -> list[BlogPostRead]:
        posts_instance = await self.repo.get_all()
        return [
            BlogPostRead.model_validate(post) for post in posts_instance
        ]
    
    async def list_user_posts(self, user_id: int) -> list[BlogPostRead]:
        posts_instance = await self.repo.get_user_posts(user_id)
        return [
            BlogPostRead.model_validate(post) for post in posts_instance
        ]

    async def get_post(self, post_id: int):
        result = await self.repo.get_by_id(post_id)
        if not result:
            raise AppException("Post not found", status_code=404)
        return BlogPostRead.model_validate(result)

    async def create_post(self, post: BlogPostCreateForm, user_id: int) -> BlogPostRead:
        # tag_instances = await self.repo.get_or_create_tags(post.tags)
        

        new_post = Post(
            title=post.title,
            content=post.content,
            excerpt=post.excerpt,
            author_id=user_id,
            # tags=tag_instances,
            series_id=post.series_id
        )
        if post.image:
            new_post.image_url = FileUploadUtils.save_image(post.image)

        result = await self.repo.add(new_post)
       
        return BlogPostRead.model_validate(result)  

    async def delete_post(self, post_id: int):
        await self.repo.delete(post_id)

    async def update_post(self, post_id: int, post_data: BlogPostCreateForm):
        post = await self.repo.get_by_id(post_id)
        tag_instances = await self.repo.get_or_create_tags(post.tags)
        post_data.tags = [ ]
        result = await self.repo.update_by_id()
        tags_pydantic: list[BlogTagRead] = [
            BlogTagRead.model_validate(tag) for tag in result.tags
        ]
        return BlogPostRead.model_validate(result) if result else None
