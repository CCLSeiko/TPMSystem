from pydantic import BaseModel, field_validator, model_validator
from typing import Optional
from datetime import date, datetime
from decimal import Decimal
import re


# 資產編號格式常數
ASSET_CODE_LEN = 12          # 總長度: 前綴4 + 年份2 + 流水號6
PREFIX_LEN = 4               # 前綴固定 4 碼
YEAR_LEN = 2                 # 西元年後 2 碼
SERIAL_LEN = 6               # 流水號 6 碼
ASSET_CODE_PATTERN = re.compile(r"^[A-Z]{4}\d{2}\d{6}$")  # 4大寫英文字母+8碼數字


# ==================== 資產類別 (Category) ====================
class CategoryBase(BaseModel):
    code: str
    name: str
    prefix: str
    description: Optional[str] = None
    sort_order: int = 0
    is_active: bool = True

    @field_validator("prefix")
    @classmethod
    def validate_prefix(cls, v: str) -> str:
        v = v.strip().upper()
        if len(v) != PREFIX_LEN:
            raise ValueError(f"前綴必須為 {PREFIX_LEN} 碼大寫英文字母，目前為 {len(v)} 碼")
        if not v.isalpha():
            raise ValueError("前綴必須全部為英文字母")
        return v

class CategoryCreate(CategoryBase):
    pass

class CategoryResponse(CategoryBase):
    id: int
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# ==================== 資產 (Assets) ====================
class AssetBase(BaseModel):
    asset_code: str
    asset_name: str
    category: Optional[str] = None
    brand: Optional[str] = None
    model: Optional[str] = None
    serial_number: Optional[str] = None
    purchase_date: Optional[date] = None
    purchase_price: Optional[Decimal] = None
    current_value: Optional[Decimal] = None
    department: Optional[str] = None
    location: Optional[str] = None
    custodian: Optional[str] = None
    status: str = "使用中"
    notes: Optional[str] = None
    disposal_reason: Optional[str] = None

    @field_validator("asset_code")
    @classmethod
    def validate_asset_code(cls, v: str) -> str:
        v = v.strip().upper()
        if len(v) != ASSET_CODE_LEN:
            raise ValueError(
                f"資產編號必須為 {ASSET_CODE_LEN} 碼"
                f"（{PREFIX_LEN}碼前綴 + {YEAR_LEN}碼年份 + {SERIAL_LEN}碼流水號），"
                f"目前為 {len(v)} 碼"
            )
        if not ASSET_CODE_PATTERN.match(v):
            raise ValueError(
                "資產編號格式錯誤：前 4 碼須為大寫英文字母，後 8 碼須為數字"
                f"（例：COMP26000001）"
            )
        return v

class AssetCreate(AssetBase):
    pass

class AssetResponse(AssetBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# ==================== 盤點 (Inventory) ====================
class InventoryBase(BaseModel):
    asset_id: Optional[int] = None
    asset_code: str
    inventory_date: date
    inventory_person: Optional[str] = None
    expected_location: Optional[str] = None
    actual_location: Optional[str] = None
    location_match: Optional[bool] = None
    status: str = "正常"
    exception_description: Optional[str] = None
    exception_result: Optional[str] = None
    notes: Optional[str] = None

class InventoryCreate(InventoryBase):
    pass

class InventoryResponse(InventoryBase):
    id: int
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# ==================== 維護 (Maintenance) ====================
class MaintenanceBase(BaseModel):
    asset_id: Optional[int] = None
    asset_code: str
    maintenance_date: date
    maintenance_type: Optional[str] = None
    description: Optional[str] = None
    cost: Optional[Decimal] = Decimal(0)
    vendor: Optional[str] = None
    person_in_charge: Optional[str] = None
    next_maintenance_date: Optional[date] = None
    notes: Optional[str] = None

class MaintenanceCreate(MaintenanceBase):
    pass

class MaintenanceResponse(MaintenanceBase):
    id: int
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# ==================== 人員 (Staff) ====================
class StaffBase(BaseModel):
    name: str
    role: str = "operator"
    department: Optional[str] = None
    responsible_area: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    is_active: Optional[bool] = True

class StaffCreate(StaffBase):
    pass

class StaffResponse(StaffBase):
    id: int
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True
