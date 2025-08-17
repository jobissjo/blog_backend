# app/api/v1/users.py
from litestar import Controller, get, post
from sqlalchemy.ext.asyncio import AsyncSession
from app.domain.users.models import User, SocialMedia
from app.domain.users.repository import UserRepository, SocialMediaRepository
from app.domain.users.service import UserService, SocialMediaService
from app.domain.users.schemas import LoginSchema, UserCreate, UserRead


class UserController(Controller):
    path = "api/v1/users"
    tags = ["Users"]

    @post("/")
    async def register_user(self, data: UserCreate, session: AsyncSession) -> UserRead:
        service = UserService(UserRepository(session))
        return await service.register_user(data)

    @get("/{user_id:str}")
    async def get_user(self, user_id: str, session: AsyncSession) -> User | None:
        service = UserService(UserRepository(session))
        return await service.get_user(user_id)
    
    @post("/login")
    async def login_user(self, data: LoginSchema, session: AsyncSession) -> UserRead:
        service = UserService(UserRepository(session))
        return await service.login_user(data)
    


class SocialMediaController(Controller):
    path = "/social-media"

    @get("/")
    async def list_social_media(self, session: AsyncSession) -> list[SocialMedia]:
        service = SocialMediaService(SocialMediaRepository(session))
        return await service.list_social_media()

    @post("/")
    async def add_social_media(self, data: SocialMedia, session: AsyncSession) -> SocialMedia:
        # 🔒 Restrict this endpoint to admin later
        service = SocialMediaService(SocialMediaRepository(session))
        return await service.add_social_media(data)
