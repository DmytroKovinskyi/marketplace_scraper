from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.schemas.scraped_data import ScrapedProductDataCreate, ScrapedProductDataUpdate, ScrapedProductDataResponse
from app.services.scraped_data import (
    create_scraped_data, get_scraped_data, get_scraped_data_list, update_scraped_data, delete_scraped_data
)
from app.dependencies import get_db
from app.services.scraper import scrape_rozetka_smartphones, save_rozetka_scraped_data, scrape_citrus_smartphones, save_citrus_scraped_data, scrape_amazon_smartphones, save_amazon_scraped_data
from app.services.product import get_product
from app.services.platform import get_platforms
from app.schemas.scraped_data import ScrapedProductDataResponse
from datetime import datetime, timedelta

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

@router.post("/rozetka/search")
def scrape_rozetka(query: str, limit: int = 10):
    """Скрейпінг смартфонів на Rozetka за запитом (query)."""
    results = scrape_rozetka_smartphones(query, limit)
    return {"results": results}

@router.post("/rozetka/scrape-and-save")
def scrape_and_save_rozetka(product_id: int, platform_id: int, query: str, limit: int = 10, db: Session = Depends(get_db)):
    scraped = scrape_rozetka_smartphones(query, limit)
    saved = save_rozetka_scraped_data(db, product_id, platform_id, scraped)
    return {"saved_count": len(saved)}

@router.post("/citrus/search")
def scrape_citrus(query: str, limit: int = 10):
    results = scrape_citrus_smartphones(query, limit)
    return {"results": results}

@router.post("/citrus/scrape-and-save")
def scrape_and_save_citrus(product_id: int, platform_id: int, query: str, limit: int = 10, db: Session = Depends(get_db)):
    scraped = scrape_citrus_smartphones(query, limit)
    saved = save_citrus_scraped_data(db, product_id, platform_id, scraped)
    return {"saved_count": len(saved)}

@router.post("/amazon/search")
def scrape_amazon(query: str, limit: int = 10):
    results = scrape_amazon_smartphones(query, limit)
    return {"results": results}

@router.post("/amazon/scrape-and-save")
def scrape_and_save_amazon(product_id: int, platform_id: int, query: str, limit: int = 10, db: Session = Depends(get_db)):
    scraped = scrape_amazon_smartphones(query, limit)
    saved = save_amazon_scraped_data(db, product_id, platform_id, scraped)
    return {"saved_count": len(saved)}

@router.get("/compare-prices/{product_id}", response_model=dict)
def get_product_prices(product_id: int, db: Session = Depends(get_db)):
    """Повертає актуальні ціни для продукту з усіх платформ (останні скрейпінги)."""
    product = get_product(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    platforms = get_platforms(db)
    result = {}
    for platform in platforms:
        # Знаходимо останній запис для кожної платформи
        data = db.query(models.ScrapedProductData).filter_by(product_id=product_id, platform_id=platform.id).order_by(models.ScrapedProductData.scraped_at.desc()).first()
        if data:
            result[platform.name] = {
                "price": data.price,
                "currency": data.currency,
                "scraped_at": data.scraped_at,
                "name_on_platform": data.name_on_platform,
                "url_on_platform": data.url_on_platform
            }
        else:
            result[platform.name] = None
    return result

@router.get("/price-history/{product_id}/{platform_id}", response_model=list)
def get_price_history(product_id: int, platform_id: int, db: Session = Depends(get_db)):
    """Повертає історію зміни цін для продукту на конкретній платформі."""
    data = db.query(models.ScrapedProductData).filter_by(product_id=product_id, platform_id=platform_id).order_by(models.ScrapedProductData.scraped_at.asc()).all()
    return [
        {
            "price": d.price,
            "currency": d.currency,
            "scraped_at": d.scraped_at,
            "name_on_platform": d.name_on_platform,
            "url_on_platform": d.url_on_platform
        }
        for d in data
    ]
