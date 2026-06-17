"""
資料庫連線 — SQLAlchemy 2.0 現代寫法

- 使用 DeclarativeBase（取代舊式 declarative_base()）
- 提供 sync / async 兩種 engine
- 透過 dependency injection 管理 session 生命週期
"""

from __future__ import annotations

from collections.abc import Generator
from typing import Any

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from core.config import get_settings

settings = get_settings()

# ── Engine ──────────────────────────────────────────────────────
engine = create_engine(
    settings.database_url,
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True,          # 連線前檢查是否有效
    echo=settings.DEBUG,         # DEBUG 模式印出 SQL
)

# ── SessionFactory ──────────────────────────────────────────────
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


# ── Base — 所有 ORM Model 的父類別 ──────────────────────────────
class Base(DeclarativeBase):
    """SQLAlchemy 2.0 Declarative Base

    所有資料表 Model 都繼承此類別。
    使用現代 Mapped[] annotation 語法定義欄位。
    """


# ── Dependency Injection — FastAPI 專用 ─────────────────────────
def get_db() -> Generator[Session, Any, None]:
    """FastAPI Depends() 用 — 每個請求一個 session，請求結束自動關閉"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
