"""
設定管理 — 集中管理所有環境變數與應用設定

使用 Pydantic BaseSettings 自動從環境變數 / .env 檔案載入。
所有模組統一從此處讀取設定，不再散落各處。
"""

from __future__ import annotations

from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache


class Settings(BaseSettings):
    """應用程式全域設定"""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # ── 資料庫 ──────────────────────────────────────────
    # 完整連線字串（docker-compose 用此模式，優先權最高）
    DATABASE_URL: str | None = None

    # 個別元件（本機開發用，僅在 DATABASE_URL 未設定時生效）
    DB_HOST: str = "db"
    DB_PORT: int = 5432
    DB_USER: str = "ams_admin"
    DB_PASSWORD: str = ""
    DB_NAME: str = "asset_management"

    # ── 應用設定 ────────────────────────────────────────
    APP_NAME: str = "資產管理系統"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False

    # CORS — 允許的前端來源（禁止使用 "*" 萬用字元）
    CORS_ORIGINS: list[str] = ["http://localhost:3002", "http://127.0.0.1:3002"]

    # ── QR Code ─────────────────────────────────────────
    BASE_ASSET_URL: str = "http://localhost:3001/assets/"

    # ── JWT 認證 ─────────────────────────────────────────
    JWT_SECRET: str = "change-me-in-production-use-random-secret"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 480  # 8 小時

    # ── 折舊預設值 ──────────────────────────────────────
    DEFAULT_DEPRECIATION_YEARS: int = 5
    DEFAULT_SALVAGE_RATE: float = 0.05

    # ── 分頁預設 ────────────────────────────────────────
    DEFAULT_PAGE_SIZE: int = 20
    MAX_PAGE_SIZE: int = 200

    @property
    def database_url(self) -> str:
        """取得資料庫連線字串，優先使用完整 URL，否則自行組合"""
        if self.DATABASE_URL:
            return self.DATABASE_URL
        return (
            f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )

    @property
    def database_url_async(self) -> str:
        """非同步連線字串（供未來 async 使用）"""
        if self.DATABASE_URL:
            return self.DATABASE_URL.replace(
                "postgresql://", "postgresql+asyncpg://"
            )
        return (
            f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )


@lru_cache()
def get_settings() -> Settings:
    """回傳快取的 Settings 單例（避免每次呼叫重新載入 .env）"""
    return Settings()
