from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from models import MaintenanceRecord
from schemas import MaintenanceCreate, MaintenanceResponse

router = APIRouter()


@router.get("/", response_model=List[MaintenanceResponse])
def list_maintenance(
    asset_id: int = None,
    maintenance_type: str = None,
    db: Session = Depends(get_db),
):
    query = db.query(MaintenanceRecord)
    if asset_id:
        query = query.filter(MaintenanceRecord.asset_id == asset_id)
    if maintenance_type:
        query = query.filter(MaintenanceRecord.maintenance_type == maintenance_type)
    return query.order_by(MaintenanceRecord.maintenance_date.desc()).all()


@router.get("/{record_id}", response_model=MaintenanceResponse)
def get_maintenance(record_id: int, db: Session = Depends(get_db)):
    record = db.query(MaintenanceRecord).filter(MaintenanceRecord.id == record_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="維護紀錄不存在")
    return record


@router.post("/", response_model=MaintenanceResponse, status_code=201)
def create_maintenance(data: MaintenanceCreate, db: Session = Depends(get_db)):
    record = MaintenanceRecord(**data.model_dump())
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


@router.put("/{record_id}", response_model=MaintenanceResponse)
def update_maintenance(record_id: int, data: MaintenanceCreate, db: Session = Depends(get_db)):
    record = db.query(MaintenanceRecord).filter(MaintenanceRecord.id == record_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="維護紀錄不存在")
    for key, value in data.model_dump().items():
        setattr(record, key, value)
    db.commit()
    db.refresh(record)
    return record
