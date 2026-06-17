"""
認證路由 — 登入、Token 刷新、使用者資訊
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from core.database import get_db
from core.auth import (
    verify_password,
    create_access_token,
    get_current_user,
    hash_password,
)
from schemas.staff import LoginRequest, TokenResponse, StaffResponse
from repositories.staff_repo import StaffRepository

router = APIRouter(prefix="/api/auth", tags=["認證"])


@router.post("/login", response_model=TokenResponse)
def login(request: LoginRequest, db: Session = Depends(get_db)):
    """使用者登入，取得 JWT Token"""
    repo = StaffRepository(db)

    # 根據 username 尋找使用者
    user = repo.find_by_username(request.username)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="帳號或密碼錯誤",
        )

    # 驗證密碼
    if not verify_password(request.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="帳號或密碼錯誤",
        )

    # 檢查帳號是否啟用
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="帳號已停用",
        )

    # 產生 Token
    access_token = create_access_token(data={"sub": str(user.id), "role": user.role})

    return TokenResponse(
        access_token=access_token,
        user=StaffResponse.model_validate(user),
    )


@router.get("/me", response_model=StaffResponse)
def get_me(current_user=Depends(get_current_user)):
    """取得當前登入使用者資訊"""
    return StaffResponse.model_validate(current_user)
