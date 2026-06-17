"""
ORM 模型包裝 — 統一匯出所有資料表模型

使用方式（三種皆可）：
  from models import Asset, Staff
  from models.asset import Asset
  from models.category import AssetCategory
"""

# ── 依序載入（無循環依賴的先載入） ──────────────────────
from models.category import AssetCategory
from models.staff import Staff

# ── 有互相關聯的在後載入 ───────────────────────────────
from models.asset import Asset
from models.inventory import InventoryRecord
from models.maintenance import MaintenanceRecord

# ── 公開 API — 與舊 models.py 相容 ─────────────────────
__all__ = [
    "AssetCategory",
    "Staff",
    "Asset",
    "InventoryRecord",
    "MaintenanceRecord",
]
