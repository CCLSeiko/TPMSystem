"""
資產編號常數與共用 Pydantic Schema
"""

from __future__ import annotations

import re
from typing import Generic, TypeVar

from pydantic import BaseModel

# ── 資產編號格式常數 ──────────────────────────────────
ASSET_CODE_LEN = 12            # 總長度: 前綴4 + 年份2 + 流水號6
PREFIX_LEN = 4                 # 前綴固定 4 碼
YEAR_LEN = 2                   # 西元年後 2 碼
SERIAL_LEN = 6                 # 流水號 6 碼
ASSET_CODE_PATTERN = re.compile(r"^[A-Z]{4}\d{2}\d{6}$")


# ── 分頁共用 Schema ───────────────────────────────────
T = TypeVar("T")


class Page(BaseModel, Generic[T]):
    """通用分頁 Response — 所有列表 API 統一格式"""

    items: list[T]
    total: int
    page: int
    size: int
    pages: int
