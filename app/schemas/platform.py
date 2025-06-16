from pydantic import BaseModel
from typing import Optional

class PlatformBase(BaseModel):
    name: str
    base_url: str
    search_url_template: str

class PlatformCreate(PlatformBase):
    pass

class PlatformUpdate(BaseModel):
    name: Optional[str] = None
    base_url: Optional[str] = None
    search_url_template: Optional[str] = None

class PlatformInDBBase(PlatformBase):
    id: int
    class Config:
        orm_mode = True

class PlatformResponse(PlatformInDBBase):
    pass
