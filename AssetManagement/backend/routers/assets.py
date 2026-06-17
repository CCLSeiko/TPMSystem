"""
資產台帳 API — 使用 AssetService 處理業務邏輯
"""

from fastapi import APIRouter, Depends, status
from typing import List

from dependencies import get_asset_service
from core.auth import get_current_user, require_permission
from schemas.asset import AssetCreate, AssetResponse
from services.asset_service import AssetService

router = APIRouter()


@router.get("/", response_model=List[AssetResponse])
def list_assets(
    category: str = None,
    status: str = None,
    department: str = None,
    svc: AssetService = Depends(get_asset_service),
):
    return svc.list_assets(category=category, status=status, department=department)


@router.get("/{asset_id}", response_model=AssetResponse)
def get_asset(
    asset_id: int,
    svc: AssetService = Depends(get_asset_service),
):
    return svc.get_by_id(asset_id)


@router.post("/", response_model=AssetResponse, status_code=status.HTTP_201_CREATED)
def create_asset(
    data: AssetCreate,
    svc: AssetService = Depends(get_asset_service),
    current_user=Depends(require_permission("write")),
):
    return svc.create_asset(data)


@router.put("/{asset_id}", response_model=AssetResponse)
def update_asset(
    asset_id: int,
    data: AssetCreate,
    svc: AssetService = Depends(get_asset_service),
    current_user=Depends(require_permission("write")),
):
    return svc.update_asset(asset_id, data)


@router.delete("/{asset_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_asset(
    asset_id: int,
    svc: AssetService = Depends(get_asset_service),
    current_user=Depends(require_permission("delete")),
):
    svc.delete_asset(asset_id)
