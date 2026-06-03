"""
更新現有類別前綴為 4 碼
"""

from sqlalchemy import text
from database import SessionLocal

# 新前綴對應
NEW_PREFIXES = {
    "電腦設備": "COMP",
    "伺服器": "SERV",
    "螢幕": "DISP",
    "印表機": "PRNT",
    "事務機": "MFP_",
    "網路設備": "NETW",
    "儲存設備": "STOR",
    "電源設備": "POWR",
    "辦公傢俱": "FURN",
    "空調設備": "HVAC",
    "行動裝置": "MOBL",
    "視聽設備": "AVEO",
    "安全設備": "SECU",
}


def main():
    db = SessionLocal()
    try:
        print("📋 更新類別前綴為 4 碼:")
        for cat_name, new_prefix in NEW_PREFIXES.items():
            result = db.execute(
                text("UPDATE asset_categories SET prefix = :prefix, code = :code WHERE name = :name"),
                {"prefix": new_prefix, "code": new_prefix, "name": cat_name},
            )
            if result.rowcount > 0:
                print(f"  ✅ {cat_name}: {new_prefix}")

        db.commit()

        # 顯示所有類別
        print(f"\n📋 更新後所有類別:")
        all_cats = db.execute(
            text("SELECT code, name, prefix FROM asset_categories ORDER BY sort_order, code")
        ).all()
        for c in all_cats:
            count = db.execute(
                text("SELECT COUNT(*) FROM assets WHERE category = :cat"), {"cat": c[1]}
            ).scalar()
            print(f"  [{c[0]:5s}] {c[1]:8s}  前綴: {c[2]:5s}  編號範例: {c[2]}000001  ({count}件)")

    except Exception as e:
        db.rollback()
        print(f"❌ 錯誤: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    main()
