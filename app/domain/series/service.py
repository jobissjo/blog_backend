# app/domain/series/service.py
from app.core.exceptions import AppException
from app.domain.series.schema import SeriesCreate, SeriesRead
from .repository import SeriesRepository
from .models import Series


class SeriesService:
    def __init__(self, repo: SeriesRepository):
        self.repo = repo

    async def list_series(self) -> list[SeriesRead]:
        try:
            series_models = await self.repo.get_all()
            return [SeriesRead.model_validate(series) for series in series_models]
        except Exception as e:
            raise AppException(f"Error retrieving series: {str(e)}", status_code=500)

    async def get_series(self, series_id: str) -> SeriesRead | None:
        result = await self.repo.get_by_id(series_id)
        return SeriesRead.model_validate(result) if result else None

    async def create_series(self, series: SeriesCreate) -> SeriesRead:
        existing_series = await self.repo.get_series_by_name(series.name)
        if existing_series:
            raise AppException(f"Series with name '{series.name}' already exists.", status_code=400)
        
        new_series = Series(
            name=series.name,
            description=series.description,
            thumbnail=series.thumbnail
        )
        series_obj = await self.repo.add(series=new_series)
        return SeriesRead.model_validate(series_obj)

    async def delete_series(self, series_id: int) -> None:
        series = await self.repo.get_by_id(series_id)
        if not series:
            raise AppException(f"Series with id {series_id} not found", status_code=404)
        
        return await self.repo.delete(series)
    
    async def update_series(self, series_id: str, series_data: SeriesCreate) -> SeriesRead:
        series = await self.repo.get_by_id(series_id)
        if not series:
            raise AppException(f"Series with id {series_id} not found", status_code=404)
        
        # Update fields using Pydantic model's data
        data = series_data.model_dump()
        for key, value in data.items():
            setattr(series, key, value)
        
        updated_series = await self.repo.add(series)
        return SeriesRead.model_validate(updated_series)
    
