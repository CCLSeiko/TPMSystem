"""
統一錯誤處理 — 集中管理 API 錯誤碼與例外處理

設計原則：
- 所有 HTTPException 走統一格式，前端可據此顯示中文錯誤訊息
- 自訂 BusinessError 攜帶 error_code，方便前端 i18n 或 log 追蹤
- 未預期的 Exception 由全域 handler 捕捉，不回拋 stack trace
"""

from __future__ import annotations

from typing import Any

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException


# ── 自訂業務例外 ────────────────────────────────────────────────

class AppError(Exception):
    """應用程式層級錯誤基底"""

    def __init__(
        self,
        message: str = "系統錯誤",
        error_code: str = "INTERNAL_ERROR",
        status_code: int = 500,
    ):
        self.message = message
        self.error_code = error_code
        self.status_code = status_code
        super().__init__(self.message)


class BusinessError(AppError):
    """業務邏輯錯誤（e.g. 資產編號重複、類別不存在）"""

    def __init__(self, message: str, error_code: str = "BUSINESS_ERROR"):
        super().__init__(message=message, error_code=error_code, status_code=400)


class NotFoundError(AppError):
    """資源不存在（e.g. 查無此資產）"""

    def __init__(self, message: str = "資源不存在", error_code: str = "NOT_FOUND"):
        super().__init__(message=message, error_code=error_code, status_code=404)


class AuthError(AppError):
    """認證 / 權限錯誤"""

    def __init__(self, message: str = "權限不足", error_code: str = "FORBIDDEN"):
        super().__init__(message=message, error_code=error_code, status_code=403)


# ── 統一 Response 格式 ──────────────────────────────────────────

def error_response(message: str, error_code: str = "ERROR") -> dict:
    """產生統一的錯誤 Response 結構"""
    return {
        "success": False,
        "error": {
            "code": error_code,
            "message": message,
        },
    }


def success_response(data: Any = None, message: str = "成功") -> dict:
    """產生統一的成功 Response 結構（選擇性使用）"""
    return {
        "success": True,
        "message": message,
        "data": data,
    }


# ── 註冊全域 Exception Handler ──────────────────────────────────

def register_error_handlers(app: FastAPI) -> None:
    """在 FastAPI 應用程式上註冊所有的錯誤處理器"""

    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(
        request: Request, exc: StarletteHTTPException
    ) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code,
            content=error_response(
                message=str(exc.detail),
                error_code=f"HTTP_{exc.status_code}",
            ),
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(
        request: Request, exc: RequestValidationError
    ) -> JSONResponse:
        # 提取第一個驗證錯誤訊息（對使用者友善）
        errors = exc.errors()
        first_error = errors[0] if errors else {}
        msg = first_error.get("msg", "輸入資料驗證失敗")

        # 如果欄位資訊可用，附加到訊息中
        loc = first_error.get("loc", [])
        if loc:
            field_path = " → ".join(str(x) for x in loc[1:])  # 跳過 'body'
            msg = f"欄位「{field_path}」: {msg}"

        return JSONResponse(
            status_code=422,
            content=error_response(
                message=msg,
                error_code="VALIDATION_ERROR",
            ),
        )

    @app.exception_handler(AppError)
    async def app_error_handler(request: Request, exc: AppError) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code,
            content=error_response(
                message=exc.message,
                error_code=exc.error_code,
            ),
        )

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(
        request: Request, exc: Exception
    ) -> JSONResponse:
        # 生產環境不回傳原始錯誤細節
        return JSONResponse(
            status_code=500,
            content=error_response(
                message="伺服器內部錯誤，請稍後再試",
                error_code="INTERNAL_ERROR",
            ),
        )
