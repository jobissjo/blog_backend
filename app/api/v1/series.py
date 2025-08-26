# app/api/v1/series.py
from litestar import Controller, get, post, delete, put
from sqlalchemy.ext.asyncio import AsyncSession
from app.domain.series.models import Series
from app.domain.series.repository import SeriesRepository
from app.domain.series.service import SeriesService
from app.domain.series.schema import SeriesCreate, SeriesRead


class SeriesController(Controller):
    path = "api/v1/series"
    tags = ["Series"]

    @get("/")
    async def list_series(self, session: AsyncSession) -> list[SeriesRead]:
        repo = SeriesRepository(session)
        service = SeriesService(repo)
        return await service.list_series()

    @get("/{series_id:int}")
    async def get_series(self, series_id: int, session: AsyncSession) -> SeriesRead | None:
        repo = SeriesRepository(session)
        service = SeriesService(repo)
        return await service.get_series(series_id)

    @post("/")
    async def create_series(self, data: SeriesCreate, session: AsyncSession) -> SeriesRead:
        repo = SeriesRepository(session)
        service = SeriesService(repo)
        return await service.create_series(data)

    @delete("/{series_id:int}")
    async def delete_series(self, series_id: int, session: AsyncSession) -> None:
        repo = SeriesRepository(session)
        service = SeriesService(repo)
        
        await service.delete_series(series_id)
    
    @put("/{series_id:int}")
    async def update_series(self, series_id: int, data: SeriesCreate, session: AsyncSession) -> SeriesRead:
        repo = SeriesRepository(session)
        service = SeriesService(repo)
        series = await service.update_series(series_id, data)
        return series
        
        
