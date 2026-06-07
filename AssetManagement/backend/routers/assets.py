from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from models import Asset, AssetCategory
from schemas import AssetCreate, AssetResponse, PREFIX_LEN

router = APIRouter()


@router.get("/", response_model=List[AssetResponse])
def list_assets(
    category: str = None,
    status: str = None,
    department: str = None,
    db: Session = Depends(get_db),
):
    query = db.query(Asset)
    if category:
        query = query.filter(Asset.category == category)
    if status:
        query = query.filter(Asset.status == status)
    if department:
        query = query.filter(Asset.department == department)
    return query.order_by(Asset.asset_code).all()


@router.get("/{asset_id}", response_model=AssetResponse)
def get_asset(asset_id: int, db: Session = Depends(get_db)):
    asset = db.query(Asset).filter(Asset.id == asset_id).first()
    if not asset:
        raise HTTPException(status_code=404, detail="資產不存在")
    return asset


@router.post("/", response_model=AssetResponse, status_code=201)
def create_asset(data: AssetCreate, db: Session = Depends(get_db)):
    # 驗證資產編號是否已存在
    existing = db.query(Asset).filter(Asset.asset_code == data.asset_code).first()
    if existing:
        raise HTTPException(status_code=400, detail="資產編號已存在")

    # 驗證前綴是否對應有效類別
    prefix = data.asset_code[:PREFIX_LEN]
    cat = db.query(AssetCategory).filter(AssetCategory.prefix == prefix).first()
    if not cat:
        raise HTTPException(
            status_code=400,
            detail=f"資產編號前綴 '{prefix}' 沒有對應的資產類別，請先建立該類別或使用正確的前綴"
        )

    asset = Asset(**data.model_dump())
    db.add(asset)
    db.commit()
    db.refresh(asset)
    return asset


@router.put("/{asset_id}", response_model=AssetResponse)
def update_asset(asset_id: int, data: AssetCreate, db: Session = Depends(get_db)):
    asset = db.query(Asset).filter(Asset.id == asset_id).first()
    if not asset:
        raise HTTPException(status_code=404, detail="資產不存在")

    # 如果資產編號有變更，驗證新編號
    if data.asset_code != asset.asset_code:
        existing = db.query(Asset).filter(Asset.asset_code == data.asset_code).first()
        if existing:
            raise HTTPException(status_code=400, detail="資產編號已存在")

        # 驗證新前綴是否對應有效類別
        prefix = data.asset_code[:PREFIX_LEN]
        cat = db.query(AssetCategory).filter(AssetCategory.prefix == prefix).first()
        if not cat:
            raise HTTPException(
                status_code=400,
                detail=f"資產編號前綴 '{prefix}' 沒有對應的資產類別"
            )

    for key, value in data.model_dump().items():
        setattr(asset, key, value)
    db.commit()
    db.refresh(asset)
    return asset


@router.delete("/{asset_id}", status_code=204)
def delete_asset(asset_id: int, db: Session = Depends(get_db)):
    asset = db.query(Asset).filter(Asset.id == asset_id).first()
    if not asset:
        raise HTTPException(status_code=404, detail="資產不存在")
    db.delete(asset)
    db.commit()
