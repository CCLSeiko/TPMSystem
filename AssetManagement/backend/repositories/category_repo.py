"""
資產類別 Repository
"""

from __future__ import annotations

from sqlalchemy.orm import Session

from models.category import AssetCategory
from repositories.base import BaseRepository


class CategoryRepository(BaseRepository[AssetCategory]):
    """資產類別資料存取層"""

    def __init__(self, db: Session):
        super().__init__(db, AssetCategory)

    def find_by_code(self, code: str) -> AssetCategory | None:
        """依類別代碼查詢"""
        return self.db.query(AssetCategory).filter(AssetCategory.code == code).first()

    def find_by_prefix(self, prefix: str) -> AssetCategory | None:
        """依編號前綴查詢（用於資產編號驗證）"""
        return (
            self.db.query(AssetCategory)
            .filter(AssetCategory.prefix == prefix)
            .first()
        )

    def get_active(self) -> list[AssetCategory]:
        """取得所有啟用的類別"""
        return (
            self.db.query(AssetCategory)
            .filter(AssetCategory.is_active == True)
            .order_by(AssetCategory.sort_order, AssetCategory.code)
            .all()
        )

    def get_max_serial(self, prefix: str, year_suffix: str) -> int | None:
        """取得指定前綴+年份的最大流水號（用於自動編號）"""
        from sqlalchemy import text

        pattern = f"^{prefix}{year_suffix}\\d{6}$"
        result = self.db.execute(
            text(
                "SELECT asset_code FROM assets "
                "WHERE asset_code ~ :pattern "
                "ORDER BY asset_code DESC LIMIT 1"
            ),
            {"pattern": pattern},
        ).scalar()
        if result:
            from schemas.common import PREFIX_LEN, YEAR_LEN
            return int(result[PREFIX_LEN + YEAR_LEN :])
        return None
