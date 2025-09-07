from typing import Optional
from pydantic import BaseModel, ConfigDict
from dataclasses import dataclass
from litestar.datastructures import UploadFile
from litestar.params import Body

class SeriesBase(BaseModel):
    name: str
    
    class Config:
        from_attributes = True


@dataclass
class SeriesCreateForm:
    name: str 
    description: str
    thumbnail: Optional[UploadFile] = None

class SeriesCreate(SeriesBase):
    description: Optional[str] = None
    thumbnail: Optional[str] = None


class SeriesRead(SeriesBase):
    id: int
    description: Optional[str] = None
    thumbnail: Optional[str] = None

    class Config:
        from_attributes = True
