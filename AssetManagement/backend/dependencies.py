"""
FastAPI Dependencies — Service 注入工廠

每個 Router 使用 Depends() 注入對應的 Service 實例。
Session 的生命週期由 core.database.get_db() 管理。
"""

from fastapi import Depends
from sqlalchemy.orm import Session

from core.database import get_db
from services import (
    AssetService,
    CategoryService,
    InventoryService,
    MaintenanceService,
    StaffService,
)


def get_asset_service(db: Session = Depends(get_db)) -> AssetService:
    return AssetService(db)


def get_category_service(db: Session = Depends(get_db)) -> CategoryService:
    return CategoryService(db)


def get_inventory_service(db: Session = Depends(get_db)) -> InventoryService:
    return InventoryService(db)


def get_maintenance_service(db: Session = Depends(get_db)) -> MaintenanceService:
    return MaintenanceService(db)


def get_staff_service(db: Session = Depends(get_db)) -> StaffService:
    return StaffService(db)
