# app/domain/series/service.py
from app.core.exceptions import AppException
from app.domain.series.schema import SeriesCreate, SeriesCreateForm, SeriesRead
from .repository import SeriesRepository
from .models import Series
from app.utils.file_upload import FileUploadUtils


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

    async def create_series(self, series_data: SeriesCreateForm) -> SeriesRead:
        existing_series = await self.repo.get_series_by_name(series_data.name)
        if existing_series:
            raise AppException(
                f"Series with name '{series_data.name}' already exists.",
                status_code=400,
            )

        series_update_data = SeriesCreate(
            name=series_data.name, description=series_data.description
        )
        if series_data.thumbnail:
            thumbnail_path = FileUploadUtils.save_image(series_data.thumbnail, "series")
            series_update_data.thumbnail = thumbnail_path
        new_series = Series(**series_update_data.model_dump())
        series_obj = await self.repo.add(series=new_series)
        return SeriesRead.model_validate(series_obj)

    async def delete_series(self, series_id: int) -> None:
        series = await self.repo.get_by_id(series_id)
        if not series:
            raise AppException(f"Series with id {series_id} not found", status_code=404)

        return await self.repo.delete(series)

    async def update_series(
        self, series_id: str, series_data: SeriesCreateForm
    ) -> SeriesRead:
        series = await self.repo.get_by_id(series_id)
        if not series:
            raise AppException(f"Series with id {series_id} not found", status_code=404)

        series_update_data = SeriesCreate(
            name=series_data.name, description=series_data.description
        )
        if series_data.thumbnail:
            thumbnail_path = FileUploadUtils.save_image(series_data.thumbnail, "series")
            series_update_data.thumbnail = thumbnail_path

        existing_series = await self.repo.get_series_by_name(series_data.name)
        if existing_series and existing_series.id != series.id:
            raise AppException(
                f"Series with name '{series_data.name}' already exists.",
                status_code=400,
            )

        updated_series = await self.repo.update_series(
            series_instance=series, series_update_data=series_update_data
        )
        return SeriesRead.model_validate(updated_series)
