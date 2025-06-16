from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ScrapedProductDataBase(BaseModel):
    product_id: int
    platform_id: int
    url_on_platform: Optional[str] = None
    name_on_platform: Optional[str] = None
    price: Optional[float] = None
    currency: Optional[str] = None
    rating: Optional[float] = None
    reviews_count: Optional[int] = None
    availability_status: Optional[str] = None
    scraped_at: Optional[datetime] = None
    search_position: Optional[int] = None

class ScrapedProductDataCreate(ScrapedProductDataBase):
    pass

class ScrapedProductDataUpdate(BaseModel):
    url_on_platform: Optional[str] = None
    name_on_platform: Optional[str] = None
    price: Optional[float] = None
    currency: Optional[str] = None
    rating: Optional[float] = None
    reviews_count: Optional[int] = None
    availability_status: Optional[str] = None
    scraped_at: Optional[datetime] = None
    search_position: Optional[int] = None

class ScrapedProductDataInDBBase(ScrapedProductDataBase):
    id: int
    class Config:
        orm_mode = True

class ScrapedProductDataResponse(ScrapedProductDataInDBBase):
    pass
