from sqlalchemy import Column, Integer, String, Text, Date, DECIMAL, Boolean, TIMESTAMP, ForeignKey
from sqlalchemy.sql import func
from database import Base


class AssetCategory(Base):
    """資產類別資料表"""
    __tablename__ = "asset_categories"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(20), unique=True, nullable=False, index=True)  # 類別代碼
    name = Column(String(100), nullable=False)                          # 類別名稱
    prefix = Column(String(10), nullable=False)                         # 編號前綴 (e.g. PC, SRV)
    description = Column(Text)
    sort_order = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    created_at = Column(TIMESTAMP, server_default=func.now())


class Staff(Base):
    """管理人員資料表"""
    __tablename__ = "staff"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    role = Column(String(20), nullable=False, default="operator")  # admin / operator / viewer
    department = Column(String(100))
    responsible_area = Column(String(200))
    phone = Column(String(20))
    email = Column(String(100))
    is_active = Column(Boolean, default=True)
    created_at = Column(TIMESTAMP, server_default=func.now())


class Asset(Base):
    """資產基本資料表"""
    __tablename__ = "assets"

    id = Column(Integer, primary_key=True, index=True)
    asset_code = Column(String(20), unique=True, nullable=False, index=True)
    asset_name = Column(String(200), nullable=False)
    category = Column(String(100), index=True)
    brand = Column(String(100))
    model = Column(String(200))
    serial_number = Column(String(100))
    purchase_date = Column(Date)
    purchase_price = Column(DECIMAL(12, 2))
    current_value = Column(DECIMAL(12, 2))
    department = Column(String(100))
    location = Column(String(200))
    custodian = Column(String(50))
    status = Column(String(20), default="使用中", index=True)  # 使用中 / 閒置 / 報廢
    notes = Column(Text)
    disposal_reason = Column(Text)                                # 報廢原因
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())


class InventoryRecord(Base):
    """盤點紀錄表"""
    __tablename__ = "inventory_records"

    id = Column(Integer, primary_key=True, index=True)
    asset_id = Column(Integer, ForeignKey("assets.id"))
    asset_code = Column(String(20), nullable=False)
    inventory_date = Column(Date, nullable=False)
    inventory_person = Column(String(50))
    expected_location = Column(String(200))
    actual_location = Column(String(200))
    location_match = Column(Boolean)
    status = Column(String(20), default="正常")  # 正常 / 異常
    exception_description = Column(Text)
    exception_result = Column(Text)
    notes = Column(Text)
    created_at = Column(TIMESTAMP, server_default=func.now())


class MaintenanceRecord(Base):
    """維護紀錄表"""
    __tablename__ = "maintenance_records"

    id = Column(Integer, primary_key=True, index=True)
    asset_id = Column(Integer, ForeignKey("assets.id"))
    asset_code = Column(String(20), nullable=False)
    maintenance_date = Column(Date, nullable=False)
    maintenance_type = Column(String(50))  # 維修 / 保養 / 耗材更換
    description = Column(Text)
    cost = Column(DECIMAL(12, 2), default=0)
    vendor = Column(String(100))
    person_in_charge = Column(String(50))
    next_maintenance_date = Column(Date)
    notes = Column(Text)
    created_at = Column(TIMESTAMP, server_default=func.now())
