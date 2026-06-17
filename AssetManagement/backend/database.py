"""
database.py（相容層）

為了讓現有 routers / models 不用全部立即改寫，
此檔案保留原始名稱，但從新的 core.database 匯出。

逐步遷移完成後可移除此檔案。
"""

from core.database import Base, SessionLocal, engine, get_db  # noqa: F401
