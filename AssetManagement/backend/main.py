"""
資產管理系統 — FastAPI 應用入口

使用新的分層架構：
  core/config.py   → 設定管理
  core/database.py → SQLAlchemy 2.0 engine + session
  core/errors.py   → 統一錯誤處理
"""

from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import text
from sqlalchemy.orm import Session

from core.config import get_settings
from core.database import engine, Base, get_db
from core.errors import register_error_handlers
from routers import assets, inventory, maintenance, staff, dashboard, categories, qrcode, auth

settings = get_settings()

# ── FastAPI 應用 ────────────────────────────────────────────────
app = FastAPI(
    title=settings.APP_NAME,
    description="固定資產管理系統後端服務 — 分層架構",
    version=settings.APP_VERSION,
)

# ── CORS ────────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Content-Type", "Authorization"],
)

# ── 註冊全域錯誤處理器 ─────────────────────────────────────────
register_error_handlers(app)

# ── 註冊路由 ────────────────────────────────────────────────────
app.include_router(auth.router)
app.include_router(assets.router, prefix="/api/assets", tags=["資產台帳"])
app.include_router(inventory.router, prefix="/api/inventory", tags=["盤點管理"])
app.include_router(maintenance.router, prefix="/api/maintenance", tags=["維修保養"])
app.include_router(staff.router, prefix="/api/staff", tags=["人員管理"])
app.include_router(dashboard.router, prefix="/api", tags=["儀表板"])
app.include_router(categories.router, prefix="/api/categories", tags=["資產類別"])
app.include_router(qrcode.router)


# ── Startup Event ───────────────────────────────────────────────
@app.on_event("startup")
def on_startup():
    """啟動時自動建立所有資料表（開發階段用，正式環境請改用 Alembic）"""
    Base.metadata.create_all(bind=engine)


# ── 根路徑 ──────────────────────────────────────────────────────
@app.get("/")
def root():
    return {
        "service": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "running",
    }


@app.get("/health")
def health_check(db: Session = Depends(get_db)):
    """健康檢查 — 確認 API 與資料庫連線正常"""
    try:
        db.execute(text("SELECT 1"))
        db_status = "connected"
    except Exception as e:
        db_status = f"error: {str(e)}"

    return {
        "status": "healthy",
        "database": db_status,
        "version": settings.APP_VERSION,
    }
