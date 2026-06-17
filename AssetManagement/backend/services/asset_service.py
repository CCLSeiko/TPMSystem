"""
資產 Service — 資產台帳的業務邏輯

職責：
- 資產新增前檢查重複 + 前綴驗證
- 資產更新時處理編號變更驗證
- 複合條件查詢
- 資產刪除
"""

from __future__ import annotations

from sqlalchemy.orm import Session

from core.errors import BusinessError, NotFoundError
from models.asset import Asset
from repositories.asset_repo import AssetRepository
from repositories.category_repo import CategoryRepository
from schemas.asset import AssetCreate
from schemas.common import PREFIX_LEN


class AssetService:
    """資產台帳業務邏輯"""

    def __init__(self, db: Session):
        self.repo = AssetRepository(db)
        self.category_repo = CategoryRepository(db)

    # ── 查詢 ───────────────────────────────────────────

    def get_by_id(self, asset_id: int) -> Asset:
        """取得單筆資產，不存在則拋錯"""
        asset = self.repo.get(asset_id)
        if not asset:
            raise NotFoundError("資產不存在")
        return asset

    def list_assets(
        self,
        category: str | None = None,
        status: str | None = None,
        department: str | None = None,
        keyword: str | None = None,
        skip: int = 0,
        limit: int = 100,
    ) -> list[Asset]:
        """複合條件查詢資產列表"""
        return self.repo.search(
            category=category,
            status=status,
            department=department,
            keyword=keyword,
            skip=skip,
            limit=limit,
        )

    # ── 新增 ───────────────────────────────────────────

    def create_asset(self, data: AssetCreate) -> Asset:
        """新增資產（含重複檢查 + 前綴驗證）"""
        # 1. 檢查資產編號是否重複
        existing = self.repo.find_by_code(data.asset_code)
        if existing:
            raise BusinessError(
                f"資產編號 '{data.asset_code}' 已存在",
                error_code="ASSET_CODE_DUPLICATE",
            )

        # 2. 驗證前綴對應有效類別
        prefix = data.asset_code[:PREFIX_LEN]
        category = self.category_repo.find_by_prefix(prefix)
        if not category:
            raise BusinessError(
                f"資產編號前綴 '{prefix}' 沒有對應的資產類別，"
                f"請先建立該類別或使用正確的前綴",
                error_code="INVALID_PREFIX",
            )

        # 3. 建立資產
        return self.repo.create(data)

    # ── 更新 ───────────────────────────────────────────

    def update_asset(self, asset_id: int, data: AssetCreate) -> Asset:
        """更新資產（處理編號變更驗證）"""
        asset = self.get_by_id(asset_id)

        # 如果資產編號有變更，驗證新編號
        if data.asset_code != asset.asset_code:
            existing = self.repo.find_by_code(data.asset_code)
            if existing:
                raise BusinessError(
                    f"資產編號 '{data.asset_code}' 已存在",
                    error_code="ASSET_CODE_DUPLICATE",
                )

            # 驗證新前綴是否對應有效類別
            prefix = data.asset_code[:PREFIX_LEN]
            category = self.category_repo.find_by_prefix(prefix)
            if not category:
                raise BusinessError(
                    f"資產編號前綴 '{prefix}' 沒有對應的資產類別",
                    error_code="INVALID_PREFIX",
                )

        updated = self.repo.update(asset_id, data)
        assert updated is not None  # 上面已用 get_by_id 檢查存在
        return updated

    # ── 刪除 ───────────────────────────────────────────

    def delete_asset(self, asset_id: int) -> None:
        """刪除資產"""
        if not self.repo.delete(asset_id):
            raise NotFoundError("資產不存在")
