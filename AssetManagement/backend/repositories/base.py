"""
Generic Base Repository — 泛型 CRUD 基底類別

所有 Repository 繼承此類別，自動取得標準 CRUD 方法。
Domain-specific 查詢則在各子類別實作。

範例：
    class AssetRepository(BaseRepository[Asset]):
        def find_by_code(self, code: str) -> Asset | None:
            return self.db.query(Asset).filter(Asset.asset_code == code).first()
"""

from __future__ import annotations

from typing import Any, Generic, TypeVar

from pydantic import BaseModel
from sqlalchemy.orm import Session

from core.database import Base

# 泛型變數 — 限定為 SQLAlchemy Model
ModelT = TypeVar("ModelT", bound=Base)


class BaseRepository(Generic[ModelT]):
    """泛型 CRUD Repository"""

    def __init__(self, db: Session, model: type[ModelT]):
        self.db = db
        self.model = model

    # ── 基本 CRUD ──────────────────────────────────────

    def get(self, id: int) -> ModelT | None:
        """依主鍵取得單筆"""
        return self.db.query(self.model).filter(self.model.id == id).first()  # type: ignore

    def get_all(
        self, skip: int = 0, limit: int = 100
    ) -> list[ModelT]:
        """取得列表（支援分頁）"""
        return self.db.query(self.model).offset(skip).limit(limit).all()

    def create(self, data: BaseModel | dict[str, Any]) -> ModelT:
        """新增一筆"""
        if isinstance(data, BaseModel):
            data = data.model_dump()
        obj = self.model(**data)
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def update(self, id: int, data: BaseModel | dict[str, Any]) -> ModelT | None:
        """更新一筆（部分更新，只送有提供的欄位）"""
        obj = self.get(id)
        if not obj:
            return None
        if isinstance(data, BaseModel):
            data = data.model_dump(exclude_unset=True)
        for key, value in data.items():
            setattr(obj, key, value)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def delete(self, id: int) -> bool:
        """刪除一筆，回傳是否成功"""
        obj = self.get(id)
        if not obj:
            return False
        self.db.delete(obj)
        self.db.commit()
        return True

    # ── 輔助方法 ───────────────────────────────────────

    def count(self) -> int:
        """取得總筆數"""
        from sqlalchemy import func
        return self.db.query(func.count(self.model.id)).scalar() or 0  # type: ignore
