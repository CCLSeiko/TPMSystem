"""
類別 Service — 資產類別的業務邏輯

職責：
- 類別新增時檢查重複（代碼/名稱）
- 自動產生下一個資產編號（12碼: 前綴4+年份2+流水號6）
"""

from __future__ import annotations

from datetime import date

from sqlalchemy.orm import Session

from core.errors import BusinessError, NotFoundError
from models.category import AssetCategory
from repositories.category_repo import CategoryRepository
from schemas.category import CategoryCreate
from schemas.common import PREFIX_LEN, YEAR_LEN


class CategoryService:
    """資產類別業務邏輯"""

    def __init__(self, db: Session):
        self.repo = CategoryRepository(db)

    # ── 查詢 ───────────────────────────────────────────

    def get_by_id(self, category_id: int) -> AssetCategory:
        """取得單筆類別"""
        cat = self.repo.get(category_id)
        if not cat:
            raise NotFoundError("類別不存在")
        return cat

    def list_categories(self) -> list[AssetCategory]:
        """取得所有類別（依 sort_order 排序）"""
        return self.repo.get_all()

    def get_active_categories(self) -> list[AssetCategory]:
        """取得所有啟用的類別"""
        return self.repo.get_active()

    # ── 新增 ───────────────────────────────────────────

    def create_category(self, data: CategoryCreate) -> AssetCategory:
        """新增類別（含重複檢查）"""
        existing = self.repo.find_by_code(data.code)
        if existing:
            raise BusinessError(
                f"類別代碼 '{data.code}' 已存在",
                error_code="CATEGORY_CODE_DUPLICATE",
            )
        return self.repo.create(data)

    # ── 更新 ───────────────────────────────────────────

    def update_category(self, category_id: int, data: CategoryCreate) -> AssetCategory:
        """更新類別"""
        cat = self.get_by_id(category_id)
        updated = self.repo.update(category_id, data)
        assert updated is not None
        return updated

    # ── 刪除 ───────────────────────────────────────────

    def delete_category(self, category_id: int) -> None:
        """刪除類別"""
        if not self.repo.delete(category_id):
            raise NotFoundError("類別不存在")

    # ── 資產編號產生 ───────────────────────────────────

    def generate_next_code(self, category_id: int) -> dict:
        """根據類別前綴+年份產生下一個可用資產編號"""
        cat = self.get_by_id(category_id)

        prefix = cat.prefix.upper()
        if len(prefix) != PREFIX_LEN:
            raise BusinessError(
                f"前綴必須為 {PREFIX_LEN} 碼，目前為 {len(prefix)} 碼",
                error_code="INVALID_PREFIX_LENGTH",
            )

        year_suffix = str(date.today().year)[-YEAR_LEN:]
        max_serial = self.repo.get_max_serial(prefix, year_suffix)

        next_num = (max_serial or 0) + 1
        if next_num > 999999:
            raise BusinessError(
                "該類別+年份的流水號已達上限 (999999)",
                error_code="SERIAL_FULL",
            )

        next_code = f"{prefix}{year_suffix}{next_num:06d}"
        return {
            "prefix": prefix,
            "year": year_suffix,
            "next_code": next_code,
            "next_number": next_num,
        }
