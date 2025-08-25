# app/domain/users/repository.py
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from .models import TempOtp, User, Profile, SocialMedia


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

    async def add_user(self, user: User) -> User:
        self.session.add(user)
        await self.session.commit()
        return user
    
    async def get_email_otp(self, email: str) -> TempOtp | None:
        result = await self.session.execute(select(TempOtp).where(TempOtp.email == email))
        return result.scalars().first()
    
    async def create_or_update_temp_otp(self, email: str, otp: str) -> None:
        email_otp = await self.get_email_otp(email)
        if email_otp:
            email_otp.otp = otp
            email_otp.generated_at = datetime.now()
            await self.session.commit()
        else:
            temp_otp = TempOtp(email=email, otp=otp, generated_at=datetime.now())
            self.session.add(temp_otp)
            await self.session.commit()


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

    