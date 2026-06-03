from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func, text

from database import get_db

router = APIRouter()


@router.get("/stats")
def get_dashboard_stats(db: Session = Depends(get_db)):
    """儀表板統計資料"""
    total_assets = db.execute(text("SELECT COUNT(*) FROM assets")).scalar() or 0
    total_inventory = db.execute(text("SELECT COUNT(*) FROM inventory_records")).scalar() or 0
    total_maintenance = db.execute(text("SELECT COUNT(*) FROM maintenance_records")).scalar() or 0
    total_staff = db.execute(text("SELECT COUNT(*) FROM staff")).scalar() or 0

    # 各狀態資產數量
    status_counts = db.execute(
        text("SELECT status, COUNT(*) as count FROM assets GROUP BY status")
    ).all()

    # 本月待維護
    upcoming_maintenance = db.execute(
        text(
            "SELECT COUNT(*) FROM maintenance_records "
            "WHERE next_maintenance_date IS NOT NULL "
            "AND next_maintenance_date <= CURRENT_DATE + INTERVAL '30 days'"
        )
    ).scalar() or 0

    # 各類別資產統計
    category_counts = db.execute(
        text("SELECT category, COUNT(*) as count FROM assets GROUP BY category")
    ).all()

    return {
        "total_assets": total_assets,
        "total_inventory_records": total_inventory,
        "total_maintenance_records": total_maintenance,
        "total_staff": total_staff,
        "assets_by_status": {row[0]: row[1] for row in status_counts},
        "upcoming_maintenance": upcoming_maintenance,
        "assets_by_category": {row[0]: row[1] for row in category_counts},
    }
