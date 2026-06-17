"""
管理人員 Repository
"""

from __future__ import annotations

from sqlalchemy.orm import Session

from models.staff import Staff
from repositories.base import BaseRepository


class StaffRepository(BaseRepository[Staff]):
    """管理人員資料存取層"""

    def __init__(self, db: Session):
        super().__init__(db, Staff)

    def find_by_username(self, username: str) -> Staff | None:
        """依登入帳號查詢"""
        return self.db.query(Staff).filter(Staff.username == username).first()

    def find_by_role(self, role: str) -> list[Staff]:
        """依角色查詢（admin/operator/viewer）"""
        return self.db.query(Staff).filter(Staff.role == role).all()

    def find_by_department(self, department: str) -> list[Staff]:
        """依部門查詢"""
        return self.db.query(Staff).filter(Staff.department == department).all()

    def get_active_staff(self) -> list[Staff]:
        """取得所有啟用中的人員"""
        return (
            self.db.query(Staff)
            .filter(Staff.is_active == True)
            .order_by(Staff.name)
            .all()
        )
