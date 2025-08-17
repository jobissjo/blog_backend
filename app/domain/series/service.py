# app/domain/series/service.py
from .repository import SeriesRepository
from .models import Series


class SeriesService:
    def __init__(self, repo: SeriesRepository):
        self.repo = repo

    async def list_series(self) -> list[Series]:
        return await self.repo.get_all()

    async def get_series(self, series_id: str) -> Series | None:
        return await self.repo.get_by_id(series_id)

    async def create_series(self, series: Series) -> Series:
        return await self.repo.add(series)

    async def delete_series(self, series: Series) -> None:
        return await self.repo.delete(series)
