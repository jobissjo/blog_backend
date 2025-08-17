from app.domain.comments.models import Comment
from app.domain.comments.repository import CommentRepository
from app.domain.comments.schemas import CommentCreate, CommentUpdate, CommentRead


class CommentService:
    def __init__(self, repo: CommentRepository):
        self.repo = repo

    async def create_comment(self, data: CommentCreate, user_id: int) -> Comment:
        comment = Comment(
            content=data.content,
            user_id=user_id,
            post_id=data.post_id
        )
        return await self.repo.create(comment)

    async def get_comment(self, comment_id: int) -> Comment | None:
        return await self.repo.get_by_id(comment_id)

    async def get_post_comments(self, post_id: int) -> list[Comment]:
        return await self.repo.get_all_by_post(post_id)

    async def update_comment(self, comment_id: int, data: CommentUpdate) -> Comment | None:
        comment = await self.repo.get_by_id(comment_id)
        if not comment:
            return None
        comment.content = data.content
        return await self.repo.update(comment)

    async def delete_comment(self, comment_id: int) -> bool:
        comment = await self.repo.get_by_id(comment_id)
        if comment:
            await self.repo.delete(comment)
            return True
        return False
