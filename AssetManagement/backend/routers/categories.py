"""
資產類別 API — 使用 CategoryService 處理業務邏輯
"""

from fastapi import APIRouter, Depends, status
from typing import List

from dependencies import get_category_service
from core.auth import get_current_user, require_permission
from schemas.category import CategoryCreate, CategoryResponse
from services.category_service import CategoryService

router = APIRouter()


@router.get("/", response_model=List[CategoryResponse])
def list_categories(
    svc: CategoryService = Depends(get_category_service),
):
    return svc.list_categories()


@router.get("/{category_id}", response_model=CategoryResponse)
def get_category(
    category_id: int,
    svc: CategoryService = Depends(get_category_service),
):
    return svc.get_by_id(category_id)


@router.post("/", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED)
def create_category(
    data: CategoryCreate,
    svc: CategoryService = Depends(get_category_service),
    current_user=Depends(require_permission("write")),
):
    return svc.create_category(data)


@router.put("/{category_id}", response_model=CategoryResponse)
def update_category(
    category_id: int,
    data: CategoryCreate,
    svc: CategoryService = Depends(get_category_service),
    current_user=Depends(require_permission("write")),
):
    return svc.update_category(category_id, data)


@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(
    category_id: int,
    svc: CategoryService = Depends(get_category_service),
    current_user=Depends(require_permission("delete")),
):
    svc.delete_category(category_id)


@router.get("/{category_id}/next-code")
def get_next_code(
    category_id: int,
    svc: CategoryService = Depends(get_category_service),
):
    return svc.generate_next_code(category_id)
