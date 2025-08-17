# app/api/v1/series.py
from litestar import Controller, get, post, delete
from sqlalchemy.ext.asyncio import AsyncSession
from app.domain.series.models import Series
from app.domain.series.repository import SeriesRepository
from app.domain.series.service import SeriesService


class SeriesController(Controller):
    path = "api/v1/series"
    tags = ["Series"]

    @get("/")
    async def list_series(self, session: AsyncSession) -> list[Series]:
        repo = SeriesRepository(session)
        service = SeriesService(repo)
        return await service.list_series()

    @get("/{series_id:str}")
    async def get_series(self, series_id: str, session: AsyncSession) -> Series | None:
        repo = SeriesRepository(session)
        service = SeriesService(repo)
        return await service.get_series(series_id)

    @post("/")
    async def create_series(self, data: Series, session: AsyncSession) -> Series:
        repo = SeriesRepository(session)
        service = SeriesService(repo)
        return await service.create_series(data)

    @delete("/{series_id:str}")
    async def delete_series(self, series_id: str, session: AsyncSession) -> None:
        repo = SeriesRepository(session)
        service = SeriesService(repo)
        series = await service.get_series(series_id)
        if not series:
            raise ValueError(f"Series with id {series_id} not found")
        await service.delete_series(series)
