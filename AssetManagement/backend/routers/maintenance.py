"""
維修保養 API — 使用 MaintenanceService 處理業務邏輯
"""

from fastapi import APIRouter, Depends, status
from typing import List

from dependencies import get_maintenance_service
from core.auth import get_current_user, require_permission
from schemas.maintenance import MaintenanceCreate, MaintenanceResponse
from services.maintenance_service import MaintenanceService

router = APIRouter()


@router.get("/", response_model=List[MaintenanceResponse])
def list_maintenance(
    asset_id: int = None,
    maintenance_type: str = None,
    svc: MaintenanceService = Depends(get_maintenance_service),
):
    return svc.list_records(asset_id=asset_id, maintenance_type=maintenance_type)


@router.get("/{record_id}", response_model=MaintenanceResponse)
def get_maintenance(
    record_id: int,
    svc: MaintenanceService = Depends(get_maintenance_service),
):
    return svc.get_by_id(record_id)


@router.post(
    "/", response_model=MaintenanceResponse, status_code=status.HTTP_201_CREATED
)
def create_maintenance(
    data: MaintenanceCreate,
    svc: MaintenanceService = Depends(get_maintenance_service),
    current_user=Depends(require_permission("write")),
):
    return svc.create_record(data)


@router.put("/{record_id}", response_model=MaintenanceResponse)
def update_maintenance(
    record_id: int,
    data: MaintenanceCreate,
    svc: MaintenanceService = Depends(get_maintenance_service),
    current_user=Depends(require_permission("write")),
):
    return svc.update_record(record_id, data)
