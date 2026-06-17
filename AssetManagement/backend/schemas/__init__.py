"""
Pydantic Schema 包裝 — 統一匯出所有資料驗證模型

使用方式（三種皆可）：
  from schemas import AssetCreate, AssetResponse
  from schemas.asset import AssetCreate, AssetResponse
  from schemas.category import CategoryCreate
"""

# ── 共用常數 ──────────────────────────────────────────
from schemas.common import (
    ASSET_CODE_LEN,
    ASSET_CODE_PATTERN,
    PREFIX_LEN,
    SERIAL_LEN,
    YEAR_LEN,
    Page,
)

# ── 類別 Schema ───────────────────────────────────────
from schemas.category import (
    CategoryBase,
    CategoryCreate,
    CategoryResponse,
)

# ── 資產 Schema ───────────────────────────────────────
from schemas.asset import (
    AssetBase,
    AssetCreate,
    AssetResponse,
)

# ── 盤點 Schema ───────────────────────────────────────
from schemas.inventory import (
    InventoryBase,
    InventoryCreate,
    InventoryResponse,
)

# ── 維護 Schema ───────────────────────────────────────
from schemas.maintenance import (
    MaintenanceBase,
    MaintenanceCreate,
    MaintenanceResponse,
)

# ── 人員 Schema ───────────────────────────────────────
from schemas.staff import (
    StaffBase,
    StaffCreate,
    StaffResponse,
)

# ── 公開 API — 與舊 schemas.py 相容 ───────────────────
__all__ = [
    # 常數
    "ASSET_CODE_LEN",
    "ASSET_CODE_PATTERN",
    "PREFIX_LEN",
    "SERIAL_LEN",
    "YEAR_LEN",
    "Page",
    # Category
    "CategoryBase",
    "CategoryCreate",
    "CategoryResponse",
    # Asset
    "AssetBase",
    "AssetCreate",
    "AssetResponse",
    # Inventory
    "InventoryBase",
    "InventoryCreate",
    "InventoryResponse",
    # Maintenance
    "MaintenanceBase",
    "MaintenanceCreate",
    "MaintenanceResponse",
    # Staff
    "StaffBase",
    "StaffCreate",
    "StaffResponse",
]
