from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from typing import List
from app.schemas.regression import RegressionModelCreate, RegressionModelUpdate, RegressionModelResponse
from app.services.regression import (
    create_regression_model, get_regression_model, get_regression_models, update_regression_model, delete_regression_model,
    train_regression_model, predict_regression
)
from app.dependencies import get_db
from app.db import models

router = APIRouter(prefix="/regression-models", tags=["regression-models"])

@router.post("/", response_model=RegressionModelResponse)
def create(model: RegressionModelCreate, db: Session = Depends(get_db)):
    return create_regression_model(db, model)

@router.get("/", response_model=List[RegressionModelResponse])
def read_models(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_regression_models(db, skip=skip, limit=limit)

@router.get("/{model_id}", response_model=RegressionModelResponse)
def read(model_id: int, db: Session = Depends(get_db)):
    db_model = get_regression_model(db, model_id)
    if not db_model:
        raise HTTPException(status_code=404, detail="Regression model not found")
    return db_model

@router.put("/{model_id}", response_model=RegressionModelResponse)
def update(model_id: int, model: RegressionModelUpdate, db: Session = Depends(get_db)):
    db_model = update_regression_model(db, model_id, model)
    if not db_model:
        raise HTTPException(status_code=404, detail="Regression model not found")
    return db_model

@router.delete("/{model_id}")
def delete(model_id: int, db: Session = Depends(get_db)):
    success = delete_regression_model(db, model_id)
    if not success:
        raise HTTPException(status_code=404, detail="Regression model not found")
    return {"ok": True}

@router.post("/train")
def train_regression(product_id: int, platform_id: int, target_variable: str, feature_variables: list = Body(...), model_name: str = None, db: Session = Depends(get_db)):
    reg_model, error = train_regression_model(db, product_id, platform_id, target_variable, feature_variables, model_name)
    if error:
        raise HTTPException(status_code=400, detail=error)
    return reg_model

@router.post("/predict/{model_id}")
def predict(model_id: int, features: dict = Body(...), db: Session = Depends(get_db)):
    model = db.query(models.RegressionModel).filter_by(id=model_id).first()
    if not model:
        raise HTTPException(status_code=404, detail="Regression model not found")
    prediction = predict_regression(model, features)
    return {"prediction": prediction}
