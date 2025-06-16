from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.schemas.scraped_data import ScrapedProductDataCreate, ScrapedProductDataUpdate, ScrapedProductDataResponse
from app.services.scraped_data import (
    create_scraped_data, get_scraped_data, get_scraped_data_list, update_scraped_data, delete_scraped_data
)
from app.dependencies import get_db

router = APIRouter(prefix="/scraped-data", tags=["scraped-data"])

@router.post("/", response_model=ScrapedProductDataResponse)
def create(data: ScrapedProductDataCreate, db: Session = Depends(get_db)):
    return create_scraped_data(db, data)

@router.get("/", response_model=List[ScrapedProductDataResponse])
def read_list(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_scraped_data_list(db, skip=skip, limit=limit)

@router.get("/{data_id}", response_model=ScrapedProductDataResponse)
def read(data_id: int, db: Session = Depends(get_db)):
    db_data = get_scraped_data(db, data_id)
    if not db_data:
        raise HTTPException(status_code=404, detail="Scraped data not found")
    return db_data

@router.put("/{data_id}", response_model=ScrapedProductDataResponse)
def update(data_id: int, data: ScrapedProductDataUpdate, db: Session = Depends(get_db)):
    db_data = update_scraped_data(db, data_id, data)
    if not db_data:
        raise HTTPException(status_code=404, detail="Scraped data not found")
    return db_data

@router.delete("/{data_id}")
def delete(data_id: int, db: Session = Depends(get_db)):
    success = delete_scraped_data(db, data_id)
    if not success:
        raise HTTPException(status_code=404, detail="Scraped data not found")
    return {"ok": True}
