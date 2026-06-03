from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from models import Staff
from schemas import StaffCreate, StaffResponse

router = APIRouter()


@router.get("/", response_model=List[StaffResponse])
def list_staff(db: Session = Depends(get_db)):
    return db.query(Staff).order_by(Staff.name).all()


@router.get("/{staff_id}", response_model=StaffResponse)
def get_staff(staff_id: int, db: Session = Depends(get_db)):
    person = db.query(Staff).filter(Staff.id == staff_id).first()
    if not person:
        raise HTTPException(status_code=404, detail="人員不存在")
    return person


@router.post("/", response_model=StaffResponse, status_code=201)
def create_staff(data: StaffCreate, db: Session = Depends(get_db)):
    person = Staff(**data.model_dump())
    db.add(person)
    db.commit()
    db.refresh(person)
    return person


@router.put("/{staff_id}", response_model=StaffResponse)
def update_staff(staff_id: int, data: StaffCreate, db: Session = Depends(get_db)):
    person = db.query(Staff).filter(Staff.id == staff_id).first()
    if not person:
        raise HTTPException(status_code=404, detail="人員不存在")
    for key, value in data.model_dump().items():
        setattr(person, key, value)
    db.commit()
    db.refresh(person)
    return person


@router.delete("/{staff_id}", status_code=204)
def delete_staff(staff_id: int, db: Session = Depends(get_db)):
    person = db.query(Staff).filter(Staff.id == staff_id).first()
    if not person:
        raise HTTPException(status_code=404, detail="人員不存在")
    db.delete(person)
    db.commit()
