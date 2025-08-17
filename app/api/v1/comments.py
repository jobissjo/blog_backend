from litestar import Controller, post, get, delete
from litestar.params import Body
from sqlalchemy.ext.asyncio import AsyncSession
from app.domain.comments.repository import CommentRepository
from app.domain.comments.service import CommentService
from app.domain.comments.schemas import CommentRead, CommentCreate


class CommentController(Controller):
    path = "api/v1/comments"
    tags = ["Comments"]

    @post("/")
    async def create_comment(
        self,
        session: AsyncSession,
        data: CommentCreate = Body(),
    ) -> CommentRead:
        repo = CommentRepository(session)
        service = CommentService(repo)
        return await service.create_comment(
            content=data["content"],
            user_id=data["user_id"],
            post_id=data["post_id"],
        )

    @get("/{comment_id:int}")
    async def get_comment(self, comment_id: int, session: AsyncSession) -> CommentRead:
        repo = CommentRepository(session)
        service = CommentService(repo)
        return await service.get_comment(comment_id)

    @get("/post/{post_id:int}")
    async def get_post_comments(
        self, post_id: int, session: AsyncSession
    ) -> list[CommentRead]:
        repo = CommentRepository(session)
        service = CommentService(repo)
        return await service.get_post_comments(post_id)

    @delete("/{comment_id:int}")
    async def delete_comment(self, comment_id: int, session: AsyncSession) -> None:
        repo = CommentRepository(session)
        service = CommentService(repo)
        await service.delete_comment(comment_id)
        return None
