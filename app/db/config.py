from app.core.config import settings
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine

engine : AsyncEngine = create_async_engine(settings.DATABASE_URL, echo=True if settings.DEBUG else False)

AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)