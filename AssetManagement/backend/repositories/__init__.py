"""
Repository 包裝 — 統一匯出所有 Repository 類別

使用方式：
    from repositories import AssetRepository, CategoryRepository
    from repositories.asset_repo import AssetRepository
"""

from repositories.base import BaseRepository
from repositories.asset_repo import AssetRepository
from repositories.category_repo import CategoryRepository
from repositories.inventory_repo import InventoryRepository
from repositories.maintenance_repo import MaintenanceRepository
from repositories.staff_repo import StaffRepository

__all__ = [
    "BaseRepository",
    "AssetRepository",
    "CategoryRepository",
    "InventoryRepository",
    "MaintenanceRepository",
    "StaffRepository",
]
