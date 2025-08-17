# app/domain/series/repository.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from .models import Series


class SeriesRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all(self) -> list[Series]:
        result = await self.session.execute(select(Series))
        return result.scalars().all()

    async def get_by_id(self, series_id: str) -> Series | None:
        return await self.session.get(Series, series_id)

    async def add(self, series: Series) -> Series:
        self.session.add(series)
        await self.session.commit()
        return series

    async def delete(self, series: Series) -> None:
        await self.session.delete(series)
        await self.session.commit()
