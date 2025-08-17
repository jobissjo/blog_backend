from app.domain.users.schemas import LoginSchema
from .repository import UserRepository, SocialMediaRepository
from .models import User, SocialMedia
from app.core.exceptions import AppException






class UserService:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    async def register_user(self, user: User) -> User:
        return await self.repo.add(user)

    async def get_user(self, user_id: str) -> User | None:
        return await self.repo.get_by_id(user_id)
    
    async def login_user(self, user: LoginSchema) -> User | None:
        user = await self.repo.get_by_username(user.username)
        if not user:
            raise AppException("User not found", status_code=404)
        return user


class SocialMediaService:
    def __init__(self, repo: SocialMediaRepository):
        self.repo = repo

    async def add_social_media(self, sm: SocialMedia) -> SocialMedia:
        return await self.repo.add(sm)

    async def list_social_media(self) -> list[SocialMedia]:
        return await self.repo.get_all()
