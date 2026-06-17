"""
Service 包裝 — 統一匯出所有 Service 類別

使用方式：
    from services import AssetService, CategoryService
    from services.asset_service import AssetService

在 Router 中用 Depends 注入：
    def get_asset_service(db: Session = Depends(get_db)) -> AssetService:
        return AssetService(db)
"""

from services.asset_service import AssetService
from services.category_service import CategoryService
from services.inventory_service import InventoryService
from services.maintenance_service import MaintenanceService
from services.staff_service import StaffService

__all__ = [
    "AssetService",
    "CategoryService",
    "InventoryService",
    "MaintenanceService",
    "StaffService",
]
