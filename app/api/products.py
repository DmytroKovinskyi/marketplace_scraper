from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.schemas.product import ProductCreate, ProductUpdate, ProductResponse
from app.services.product import (
    create_product, get_product, get_products, update_product, delete_product
)
from app.dependencies import get_db

router = APIRouter(prefix="/products", tags=["products"])

@router.post("/", response_model=ProductResponse)
def create(product: ProductCreate, db: Session = Depends(get_db)):
    return create_product(db, product)

@router.get("/", response_model=List[ProductResponse])
def read_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_products(db, skip=skip, limit=limit)

@router.get("/{product_id}", response_model=ProductResponse)
def read_product(product_id: int, db: Session = Depends(get_db)):
    db_product = get_product(db, product_id)
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product

@router.put("/{product_id}", response_model=ProductResponse)
def update(product_id: int, product: ProductUpdate, db: Session = Depends(get_db)):
    db_product = update_product(db, product_id, product)
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product

@router.delete("/{product_id}")
def delete(product_id: int, db: Session = Depends(get_db)):
    success = delete_product(db, product_id)
    if not success:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"ok": True}
