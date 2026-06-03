from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime
from decimal import Decimal


# ==================== 資產類別 (Category) ====================
class CategoryBase(BaseModel):
    code: str
    name: str
    prefix: str
    description: Optional[str] = None
    sort_order: int = 0
    is_active: bool = True

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
