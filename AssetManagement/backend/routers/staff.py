"""
管理人員 API — 使用 StaffService 處理業務邏輯
"""

from fastapi import APIRouter, Depends, status
from typing import List

from dependencies import get_staff_service
from core.auth import get_current_user, require_role
from schemas.staff import StaffCreate, StaffResponse, StaffUpdate
from services.staff_service import StaffService

router = APIRouter()


@router.get("/", response_model=List[StaffResponse])
def list_staff(
    svc: StaffService = Depends(get_staff_service),
):
    return svc.list_staff()


@router.get("/{staff_id}", response_model=StaffResponse)
def get_staff(
    staff_id: int,
    svc: StaffService = Depends(get_staff_service),
):
    return svc.get_by_id(staff_id)


@router.post("/", response_model=StaffResponse, status_code=status.HTTP_201_CREATED)
def create_staff(
    data: StaffCreate,
    svc: StaffService = Depends(get_staff_service),
    current_user=Depends(require_role("admin")),
):
    return svc.create_staff(data)


@router.put("/{staff_id}", response_model=StaffResponse)
def update_staff(
    staff_id: int,
    data: StaffUpdate,
    svc: StaffService = Depends(get_staff_service),
    current_user=Depends(require_role("admin")),
):
    return svc.update_staff(staff_id, data)


@router.delete("/{staff_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_staff(
    staff_id: int,
    svc: StaffService = Depends(get_staff_service),
    current_user=Depends(require_role("admin")),
):
    svc.delete_staff(staff_id)
