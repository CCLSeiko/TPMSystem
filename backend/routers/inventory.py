from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from models import InventoryRecord
from schemas import InventoryCreate, InventoryResponse

router = APIRouter()


@router.get("/", response_model=List[InventoryResponse])
def list_inventory(
    asset_id: int = None,
    status: str = None,
    db: Session = Depends(get_db),
):
    query = db.query(InventoryRecord)
    if asset_id:
        query = query.filter(InventoryRecord.asset_id == asset_id)
    if status:
        query = query.filter(InventoryRecord.status == status)
    return query.order_by(InventoryRecord.inventory_date.desc()).all()


@router.get("/{record_id}", response_model=InventoryResponse)
def get_inventory(record_id: int, db: Session = Depends(get_db)):
    record = db.query(InventoryRecord).filter(InventoryRecord.id == record_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="盤點紀錄不存在")
    return record


@router.post("/", response_model=InventoryResponse, status_code=201)
def create_inventory(data: InventoryCreate, db: Session = Depends(get_db)):
    record = InventoryRecord(**data.model_dump())
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


@router.put("/{record_id}", response_model=InventoryResponse)
def update_inventory(record_id: int, data: InventoryCreate, db: Session = Depends(get_db)):
    record = db.query(InventoryRecord).filter(InventoryRecord.id == record_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="盤點紀錄不存在")
    for key, value in data.model_dump().items():
        setattr(record, key, value)
    db.commit()
    db.refresh(record)
    return record
