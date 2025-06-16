from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime

class RegressionModelBase(BaseModel):
    name: str
    target_variable: str
    feature_variables: List[str]
    coefficients_json: Optional[Dict[str, Any]] = None
    intercept: Optional[float] = None
    r_squared: Optional[float] = None
    last_trained_at: Optional[datetime] = None
    platform_id: Optional[int] = None

class RegressionModelCreate(RegressionModelBase):
    pass

class RegressionModelUpdate(BaseModel):
    name: Optional[str] = None
    target_variable: Optional[str] = None
    feature_variables: Optional[List[str]] = None
    coefficients_json: Optional[Dict[str, Any]] = None
    intercept: Optional[float] = None
    r_squared: Optional[float] = None
    last_trained_at: Optional[datetime] = None
    platform_id: Optional[int] = None

class RegressionModelInDBBase(RegressionModelBase):
    id: int
    class Config:
        orm_mode = True

class RegressionModelResponse(RegressionModelInDBBase):
    pass
