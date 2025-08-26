import msgspec
from typing import Optional


class SeriesBase(msgspec.Struct):
    name: str
    


class SeriesCreate(SeriesBase):
    description: Optional[str] = None
    thumbnail: Optional[str] = None


class SeriesRead(SeriesBase):
    id: str
    description: Optional[str] = None
    thumbnail: Optional[str] = None
