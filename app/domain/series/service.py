# app/domain/series/service.py
import msgspec
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
            series_read_list = []
            for series in series_models:
                series_read = SeriesRead(
                    id=series.id,
                    name=series.name,
                    description=series.description,
                    thumbnail=series.thumbnail
                )
                series_read_list.append(series_read)
            
            return series_read_list
        except Exception as e:
            raise AppException(f"Error retrieving series: {str(e)}", status_code=500)

    async def get_series(self, series_id: str) -> SeriesRead | None:
        result = await self.repo.get_by_id(series_id)
        if result:
            return SeriesRead(
                id=result.id,
                name=result.name,
                description=result.description,
                thumbnail=result.thumbnail
            )
        return None

    async def create_series(self, series: SeriesCreate) -> SeriesRead:
        existing_series = await self.repo.get_series_by_name(series.name)
        if existing_series:
            raise AppException(f"Series with name '{series.name}' already exists.", status_code=400)
        series = Series(name=series.name, description=series.description, thumbnail=series.thumbnail)
        series_obj =  await self.repo.add(series=series)
        return SeriesRead(
            id=series_obj.id,
            name=series_obj.name,
            description=series_obj.description,
            thumbnail=series_obj.thumbnail
        )

    async def delete_series(self, series_id: int) -> None:
        series = await self.repo.get_by_id(series_id)
        if not series:
            raise AppException(f"Series with id {series_id} not found", status_code=404)
        
        return await self.repo.delete(series)
    
    async def update_series(self, series_id: str, series_data: SeriesCreate) -> SeriesRead:
        series = await self.repo.get_by_id(series_id)
        if not series:
            raise AppException(f"Series with id {series_id} not found", status_code=404)
        
        # Update fields
        series.name = series_data.name
        series.description = series_data.description
        series.thumbnail = series_data.thumbnail
        
        updated_series = await self.repo.add(series)
        return SeriesRead(
            id=updated_series.id,
            name=updated_series.name,
            description=updated_series.description,
            thumbnail=updated_series.thumbnail
        )
    
