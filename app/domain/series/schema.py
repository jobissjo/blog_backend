import msgspec
from typing import Optional


class SeriesBase(msgspec.Struct):
    name: str
    description: Optional[str] = None
    thumbnail: Optional[str] = None


class SeriesCreate(SeriesBase):
    pass


class SeriesRead(SeriesBase):
    id: str
