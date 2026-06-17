"""
models.py（相容層）

為了讓現有 routers 不用全部立即改寫，
此檔案保留原有名稱，但從新的 models/ 套件重新匯出。

逐步遷移完成後可移除此檔案。
"""

from models import (        # noqa: F401
    Asset,
    AssetCategory,
    InventoryRecord,
    MaintenanceRecord,
    Staff,
)
