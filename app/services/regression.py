from sqlalchemy.orm import Session
from app.db import models
from app.schemas.regression import RegressionModelCreate, RegressionModelUpdate
from typing import List, Optional
import statsmodels.api as sm
from datetime import datetime
from sqlalchemy import and_
import pandas as pd
import numpy as np

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

def train_regression_model(db: Session, product_id: int, platform_id: int, target_variable: str, feature_variables: list, model_name: str = None):
    # Вибірка даних
    query = db.query(models.ScrapedProductData).filter(
        and_(models.ScrapedProductData.product_id == product_id, models.ScrapedProductData.platform_id == platform_id)
    )
    data = query.all()
    if not data or len(data) < 5:
        return None, "Not enough data for regression"
    df = pd.DataFrame([{f: getattr(d, f) for f in feature_variables + [target_variable]} for d in data])
    df = df.dropna()
    if df.shape[0] < 5:
        return None, "Not enough valid rows for regression"
    X = df[feature_variables]
    y = df[target_variable]
    X = sm.add_constant(X)
    model = sm.OLS(y, X).fit()
    # Зберігаємо модель у БД
    reg_model = models.RegressionModel(
        name=model_name or f"Regression for product {product_id} on platform {platform_id}",
        target_variable=target_variable,
        feature_variables=feature_variables,
        coefficients_json=dict(model.params),
        intercept=model.params["const"] if "const" in model.params else None,
        r_squared=model.rsquared,
        last_trained_at=datetime.utcnow(),
        platform_id=platform_id
    )
    db.add(reg_model)
    db.commit()
    db.refresh(reg_model)
    return reg_model, None

def predict_regression(model: models.RegressionModel, features: dict):
    # features: dict з іменами фіч
    coefs = model.coefficients_json.copy()
    intercept = model.intercept or coefs.pop("const", 0)
    x = np.array([features.get(f, 0) for f in model.feature_variables])
    coef_arr = np.array([coefs.get(f, 0) for f in model.feature_variables])
    pred = float(np.dot(x, coef_arr) + intercept)
    return pred
