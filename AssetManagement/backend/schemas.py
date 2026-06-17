"""
schemas.py（相容層）

為了讓現有 routers 不用全部立即改寫，
此檔案保留原有名稱，但從新的 schemas/ 套件重新匯出。

逐步遷移完成後可移除此檔案。
"""

from schemas import (        # noqa: F401
    ASSET_CODE_LEN,
    ASSET_CODE_PATTERN,
    AssetBase,
    AssetCreate,
    AssetResponse,
    CategoryBase,
    CategoryCreate,
    CategoryResponse,
    InventoryBase,
    InventoryCreate,
    InventoryResponse,
    MaintenanceBase,
    MaintenanceCreate,
    MaintenanceResponse,
    PREFIX_LEN,
    SERIAL_LEN,
    StaffBase,
    StaffCreate,
    StaffResponse,
    YEAR_LEN,
)
