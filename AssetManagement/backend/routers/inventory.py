"""
盤點管理 API — 使用 InventoryService 處理業務邏輯
"""

from fastapi import APIRouter, Depends, status
from typing import List

from dependencies import get_inventory_service
from core.auth import get_current_user, require_permission
from schemas.inventory import InventoryCreate, InventoryResponse
from services.inventory_service import InventoryService

router = APIRouter()


@router.get("/", response_model=List[InventoryResponse])
def list_inventory(
    asset_id: int = None,
    status: str = None,
    svc: InventoryService = Depends(get_inventory_service),
):
    return svc.list_records(asset_id=asset_id, status=status)


@router.get("/{record_id}", response_model=InventoryResponse)
def get_inventory(
    record_id: int,
    svc: InventoryService = Depends(get_inventory_service),
):
    return svc.get_by_id(record_id)


@router.post(
    "/", response_model=InventoryResponse, status_code=status.HTTP_201_CREATED
)
def create_inventory(
    data: InventoryCreate,
    svc: InventoryService = Depends(get_inventory_service),
    current_user=Depends(require_permission("write")),
):
    return svc.create_record(data)


@router.put("/{record_id}", response_model=InventoryResponse)
def update_inventory(
    record_id: int,
    data: InventoryCreate,
    svc: InventoryService = Depends(get_inventory_service),
    current_user=Depends(require_permission("write")),
):
    return svc.update_record(record_id, data)
