from typing import Optional
from pydantic import BaseModel, ConfigDict
from dataclasses import dataclass
from litestar.datastructures import UploadFile
from litestar.params import Body

class SeriesBase(BaseModel):
    name: str
    
    model_config = ConfigDict(from_attributes=True)


@dataclass
class SeriesCreateForm:
    description: str
    name: str 
    thumbnail: Optional[UploadFile] = None

class SeriesCreate(SeriesBase):
    description: Optional[str] = None
    thumbnail: Optional[str] = None


class SeriesRead(SeriesBase):
    id: int
    description: Optional[str] = None
    thumbnail: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)
