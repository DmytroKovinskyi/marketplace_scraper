from pydantic import BaseModel
from typing import Optional

class ProductBase(BaseModel):
    global_query_name: str
    description: Optional[str] = None

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    global_query_name: Optional[str] = None
    description: Optional[str] = None

class ProductInDBBase(ProductBase):
    id: int
    class Config:
        orm_mode = True

class ProductResponse(ProductInDBBase):
    pass
