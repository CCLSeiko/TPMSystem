"""
資產 Repository
"""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel
from sqlalchemy.orm import Session

from models.asset import Asset
from repositories.base import BaseRepository


class AssetRepository(BaseRepository[Asset]):
    """資產資料存取層"""

    def __init__(self, db: Session):
        super().__init__(db, Asset)

    # ── 領域查詢 ───────────────────────────────────────

    def find_by_code(self, code: str) -> Asset | None:
        """依資產編號查詢"""
        return self.db.query(Asset).filter(Asset.asset_code == code).first()

    def find_by_status(self, status: str, skip: int = 0, limit: int = 100) -> list[Asset]:
        """依狀態查詢"""
        return (
            self.db.query(Asset)
            .filter(Asset.status == status)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def find_by_department(self, department: str) -> list[Asset]:
        """依部門查詢"""
        return self.db.query(Asset).filter(Asset.department == department).all()

    def find_by_category(self, category: str) -> list[Asset]:
        """依類別查詢"""
        return self.db.query(Asset).filter(Asset.category == category).all()

    def search(
        self,
        category: str | None = None,
        status: str | None = None,
        department: str | None = None,
        keyword: str | None = None,
        skip: int = 0,
        limit: int = 100,
    ) -> list[Asset]:
        """複合條件查詢"""
        query = self.db.query(Asset)
        if category:
            query = query.filter(Asset.category == category)
        if status:
            query = query.filter(Asset.status == status)
        if department:
            query = query.filter(Asset.department == department)
        if keyword:
            like = f"%{keyword}%"
            query = query.filter(
                Asset.asset_name.ilike(like)
                | Asset.asset_code.ilike(like)
                | Asset.brand.ilike(like)
                | Asset.model.ilike(like)
            )
        return query.order_by(Asset.asset_code).offset(skip).limit(limit).all()

    def create_with_validation(
        self, data: BaseModel | dict[str, Any]
    ) -> Asset | None:
        """新增資產（含重複檢查），回傳 None 表示已存在"""
        if isinstance(data, BaseModel):
            code = data.asset_code
        else:
            code = data.get("asset_code", "")
        existing = self.find_by_code(code)
        if existing:
            return None
        return self.create(data)
