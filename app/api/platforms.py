from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.schemas.platform import PlatformCreate, PlatformUpdate, PlatformResponse
from app.services.platform import (
    create_platform, get_platform, get_platforms, update_platform, delete_platform
)
from app.dependencies import get_db

router = APIRouter(prefix="/platforms", tags=["platforms"])

@router.post("/", response_model=PlatformResponse)
def create(platform: PlatformCreate, db: Session = Depends(get_db)):
    return create_platform(db, platform)

@router.get("/", response_model=List[PlatformResponse])
def read_platforms(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_platforms(db, skip=skip, limit=limit)

@router.get("/{platform_id}", response_model=PlatformResponse)
def read_platform(platform_id: int, db: Session = Depends(get_db)):
    db_platform = get_platform(db, platform_id)
    if not db_platform:
        raise HTTPException(status_code=404, detail="Platform not found")
    return db_platform

@router.put("/{platform_id}", response_model=PlatformResponse)
def update(platform_id: int, platform: PlatformUpdate, db: Session = Depends(get_db)):
    db_platform = update_platform(db, platform_id, platform)
    if not db_platform:
        raise HTTPException(status_code=404, detail="Platform not found")
    return db_platform

@router.delete("/{platform_id}")
def delete(platform_id: int, db: Session = Depends(get_db)):
    success = delete_platform(db, platform_id)
    if not success:
        raise HTTPException(status_code=404, detail="Platform not found")
    return {"ok": True}
