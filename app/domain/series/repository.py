# app/domain/series/repository.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from .models import Series


class SeriesRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all(self) -> list[Series]:
        result = await self.session.execute(select(Series))
        print('hhhhhhhhhhhhhrrrrrrrrrrre')
        return result.scalars().all()

    async def get_by_id(self, series_id: str) -> Series | None:
        result = await self.session.execute(select(Series).where(Series.id == series_id))
        return result.scalar_one_or_none()
    
    async def get_series_by_name(self, name: str) -> Series | None:
        result = await self.session.execute(select(Series).where(Series.name == name))
        return result.scalar_one_or_none()

    async def add(self, series: Series) -> Series:
        self.session.add(series)
        await self.session.commit()
        return series

        await self.session.delete(series)
    async def delete(self, series: Series) -> None:
        await self.session.commit()
