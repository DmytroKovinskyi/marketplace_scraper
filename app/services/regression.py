from sqlalchemy.orm import Session
from app.db import models
from app.schemas.regression import RegressionModelCreate, RegressionModelUpdate
from typing import List, Optional

def create_regression_model(db: Session, model: RegressionModelCreate) -> models.RegressionModel:
    db_model = models.RegressionModel(**model.dict())
    db.add(db_model)
    db.commit()
    db.refresh(db_model)
    return db_model

def get_regression_model(db: Session, model_id: int) -> Optional[models.RegressionModel]:
    return db.query(models.RegressionModel).filter(models.RegressionModel.id == model_id).first()

def get_regression_models(db: Session, skip: int = 0, limit: int = 100) -> List[models.RegressionModel]:
    return db.query(models.RegressionModel).offset(skip).limit(limit).all()

def update_regression_model(db: Session, model_id: int, model: RegressionModelUpdate) -> Optional[models.RegressionModel]:
    db_model = get_regression_model(db, model_id)
    if not db_model:
        return None
    for field, value in model.dict(exclude_unset=True).items():
        setattr(db_model, field, value)
    db.commit()
    db.refresh(db_model)
    return db_model

def delete_regression_model(db: Session, model_id: int) -> bool:
    db_model = get_regression_model(db, model_id)
    if not db_model:
        return False
    db.delete(db_model)
    db.commit()
    return True
