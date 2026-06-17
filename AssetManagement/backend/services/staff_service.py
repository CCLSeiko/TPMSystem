"""
人員 Service — 管理人員的業務邏輯

職責：
- 人員 CRUD
- 依角色/部門查詢
- 密碼雜湊處理
"""

from __future__ import annotations

from sqlalchemy.orm import Session

from core.errors import NotFoundError, BusinessError
from core.auth import hash_password
from models.staff import Staff
from repositories.staff_repo import StaffRepository
from schemas.staff import StaffCreate, StaffUpdate


class StaffService:
    """管理人員業務邏輯"""

    def __init__(self, db: Session):
        self.repo = StaffRepository(db)

    def get_by_id(self, staff_id: int) -> Staff:
        person = self.repo.get(staff_id)
        if not person:
            raise NotFoundError("人員不存在")
        return person

    def list_staff(self) -> list[Staff]:
        return self.repo.get_all()

    def create_staff(self, data: StaffCreate) -> Staff:
        # 檢查 username 是否已存在
        existing = self.repo.find_by_username(data.username)
        if existing:
            raise BusinessError("ACCOUNT_EXISTS", f"帳號 {data.username} 已存在")

        # 建立人員（密碼雜湊）
        staff_dict = data.model_dump()
        password = staff_dict.pop("password")
        staff_dict["password_hash"] = hash_password(password)

        return self.repo.create(staff_dict)

    def update_staff(self, staff_id: int, data: StaffUpdate) -> Staff:
        person = self.get_by_id(staff_id)
        update_data = data.model_dump(exclude_unset=True)

        # 如果有更新密碼，進行雜湊
        if "password" in update_data:
            password = update_data.pop("password")
            update_data["password_hash"] = hash_password(password)

        updated = self.repo.update(staff_id, update_data)
        assert updated is not None
        return updated

    def delete_staff(self, staff_id: int) -> None:
        if not self.repo.delete(staff_id):
            raise NotFoundError("人員不存在")
