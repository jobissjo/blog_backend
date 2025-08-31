from typing import Optional
from pydantic import BaseModel


class SeriesBase(BaseModel):
    name: str
    
    class Config:
        from_attributes = True


class SeriesCreate(SeriesBase):
    description: Optional[str] = None
    thumbnail: Optional[str] = None


class SeriesRead(SeriesBase):
    id: str
    description: Optional[str] = None
    thumbnail: Optional[str] = None

    class Config:
        from_attributes = True
