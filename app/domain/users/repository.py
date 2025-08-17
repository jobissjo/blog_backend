# app/domain/users/repository.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from .models import User, Profile, SocialMedia


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, user_id: str) -> User | None:
        return await self.session.get(User, user_id)

    async def get_by_email(self, email: str) -> User | None:
        result = await self.session.execute(select(User).where(User.email == email))
        return result.scalars().first()
    
    async def get_by_username(self, username: str) -> User | None:
        result = await self.session.execute(select(User).where(User.username == username))
        return result.scalars().first()

    async def add(self, user: User) -> User:
        self.session.add(user)
        await self.session.commit()
        return user


class SocialMediaRepository:
    """Admin only: manage available social media types"""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all(self) -> list[SocialMedia]:
        result = await self.session.execute(select(SocialMedia))
        return result.scalars().all()

    async def add(self, sm: SocialMedia) -> SocialMedia:
        self.session.add(sm)
        await self.session.commit()
        return sm
