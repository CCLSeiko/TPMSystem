from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import List

from database import get_db
from models import AssetCategory
from schemas import CategoryCreate, CategoryResponse

router = APIRouter()


@router.get("/", response_model=List[CategoryResponse])
def list_categories(db: Session = Depends(get_db)):
    return db.query(AssetCategory).order_by(AssetCategory.sort_order, AssetCategory.code).all()


@router.get("/{category_id}", response_model=CategoryResponse)
def get_category(category_id: int, db: Session = Depends(get_db)):
    cat = db.query(AssetCategory).filter(AssetCategory.id == category_id).first()
    if not cat:
        raise HTTPException(status_code=404, detail="類別不存在")
    return cat


@router.post("/", response_model=CategoryResponse, status_code=201)
def create_category(data: CategoryCreate, db: Session = Depends(get_db)):
    existing = db.query(AssetCategory).filter(
        (AssetCategory.code == data.code) | (AssetCategory.name == data.name)
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="類別代碼或名稱已存在")
    cat = AssetCategory(**data.model_dump())
    db.add(cat)
    db.commit()
    db.refresh(cat)
    return cat


@router.put("/{category_id}", response_model=CategoryResponse)
def update_category(category_id: int, data: CategoryCreate, db: Session = Depends(get_db)):
    cat = db.query(AssetCategory).filter(AssetCategory.id == category_id).first()
    if not cat:
        raise HTTPException(status_code=404, detail="類別不存在")
    for key, value in data.model_dump().items():
        setattr(cat, key, value)
    db.commit()
    db.refresh(cat)
    return cat


@router.delete("/{category_id}", status_code=204)
def delete_category(category_id: int, db: Session = Depends(get_db)):
    cat = db.query(AssetCategory).filter(AssetCategory.id == category_id).first()
    if not cat:
        raise HTTPException(status_code=404, detail="類別不存在")
    db.delete(cat)
    db.commit()


@router.get("/{category_id}/next-code")
def get_next_code(category_id: int, db: Session = Depends(get_db)):
    """根據類別前綴+年份產生下一個可用資產編號 (12碼: 前綴4+年份2+流水號6)"""
    cat = db.query(AssetCategory).filter(AssetCategory.id == category_id).first()
    if not cat:
        raise HTTPException(status_code=404, detail="類別不存在")

    prefix = cat.prefix
    year_suffix = str(__import__("datetime").date.today().year)[-2:]  # 西元年後兩碼

    # 找出該前綴+年份的最大現有編號
    pattern = f"^{prefix}{year_suffix}\\d{{6}}$"
    result = db.execute(
        text("""
            SELECT asset_code FROM assets
            WHERE asset_code ~ :pattern
            ORDER BY asset_code DESC
            LIMIT 1
        """),
        {"pattern": pattern},
    ).scalar()

    if result:
        # 提取流水號部分（跳過前綴4碼+年份2碼）
        num = int(result[len(prefix) + 2:]) + 1
    else:
        num = 1

    next_code = f"{prefix}{year_suffix}{num:06d}"
    return {"prefix": prefix, "year": year_suffix, "next_code": next_code, "next_number": num}
