"""
JWT 認證模組 — Token 產生、驗證、密碼雜湊

提供完整 RBAC (Role-Based Access Control) 支援：
- admin:    管理員（全部權限）
- operator: 操作員（CRUD 資產、盤點、維護）
- viewer:   檢視者（唯讀）
"""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Optional

import jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from core.config import get_settings
from core.database import get_db

settings = get_settings()

# ── 密碼雜湊 ────────────────────────────────────────────────────
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# ── OAuth2 設定 ─────────────────────────────────────────────────
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


# ── JWT 設定 ─────────────────────────────────────────────────────
def get_jwt_secret():
    """取得 JWT 密鑰"""
    return settings.JWT_SECRET


def get_jwt_algorithm():
    """取得 JWT 演算法"""
    return settings.JWT_ALGORITHM


def get_token_expire_minutes():
    """取得 Token 過期時間（分鐘）"""
    return settings.ACCESS_TOKEN_EXPIRE_MINUTES


def hash_password(password: str) -> str:
    """密碼雜湊"""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """驗證密碼"""
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """產生 JWT access token"""
    to_encode = data.copy()
    expire_minutes = get_token_expire_minutes()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=expire_minutes))
    to_encode.update({"exp": expire})
    secret = get_jwt_secret()
    algorithm = get_jwt_algorithm()
    return jwt.encode(to_encode, secret, algorithm=algorithm)


def decode_access_token(token: str) -> dict:
    """解碼 JWT token"""
    secret = get_jwt_secret()
    algorithm = get_jwt_algorithm()
    try:
        payload = jwt.decode(token, secret, algorithms=[algorithm])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token 已過期，請重新登入",
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="無效的 Token",
        )


# ── Role 權限定義 ──────────────────────────────────────────────
ROLE_PERMISSIONS = {
    "admin": ["read", "write", "delete", "manage_users"],
    "operator": ["read", "write"],
    "viewer": ["read"],
}


def check_permission(role: str, required_permission: str) -> bool:
    """檢查角色是否具有所需權限"""
    permissions = ROLE_PERMISSIONS.get(role, [])
    return required_permission in permissions


# ── FastAPI Dependencies ────────────────────────────────────────
def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
):
    """從 JWT token 取得當前使用者"""
    from repositories.staff_repo import StaffRepository

    payload = decode_access_token(token)
    staff_id_str: str = payload.get("sub")
    if staff_id_str is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token 中缺少使用者資訊",
        )
    staff_id = int(staff_id_str)

    repo = StaffRepository(db)
    user = repo.get(staff_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="使用者不存在",
        )
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="帳號已停用",
        )

    return user


def require_role(*allowed_roles: str):
    """角色驗證 Dependency Factory"""
    def role_checker(current_user=Depends(get_current_user)):
        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"權限不足，需要角色: {', '.join(allowed_roles)}",
            )
        return current_user
    return role_checker


def require_permission(permission: str):
    """權限驗證 Dependency Factory"""
    def perm_checker(current_user=Depends(get_current_user)):
        if not check_permission(current_user.role, permission):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"權限不足，需要: {permission}",
            )
        return current_user
    return perm_checker
