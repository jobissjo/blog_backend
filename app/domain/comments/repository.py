from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.domain.comments.models import Comment


class CommentRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, comment: Comment) -> Comment:
        self.session.add(comment)
        await self.session.commit()
        await self.session.refresh(comment)
        return comment

    async def get_by_id(self, comment_id: int) -> Comment | None:
        result = await self.session.execute(select(Comment).where(Comment.id == comment_id))
        return result.scalar_one_or_none()

    async def get_all_by_post(self, post_id: int) -> list[Comment]:
        result = await self.session.execute(select(Comment).where(Comment.post_id == post_id))
        return result.scalars().all()

    async def delete(self, comment: Comment) -> None:
        await self.session.delete(comment)
        await self.session.commit()
