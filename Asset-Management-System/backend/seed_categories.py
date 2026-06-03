"""
從現有資產資料自動建立類別與對應前綴
"""

from sqlalchemy import text
from database import SessionLocal

# 類別代碼與 4 碼前綴對應表
CATEGORY_MAP = {
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

PREFIX_OVERRIDE = {}


def main():
    db = SessionLocal()
    try:
        # 取得所有不重複的類別
        rows = db.execute(
            text("SELECT DISTINCT category FROM assets WHERE category IS NOT NULL ORDER BY category")
        ).all()

        print(f"📋 從資產資料中發現 {len(rows)} 個類別:")
        created = 0
        for (cat_name,) in rows:
            if cat_name in CATEGORY_MAP:
                prefix = CATEGORY_MAP[cat_name]
                code = prefix
                desc = cat_name
            else:
                # 自動產生 4 碼前綴
                prefix = (cat_name[:2].upper() + "XX")[:4]
                code = prefix
                desc = cat_name

            # 檢查是否已存在
            existing = db.execute(
                text("SELECT id FROM asset_categories WHERE name = :name OR code = :code"),
                {"name": cat_name, "code": code},
            ).scalar()

            if existing:
                print(f"  ✅ {cat_name} -> {prefix} (已存在)")
            else:
                db.execute(
                    text("""
                        INSERT INTO asset_categories (code, name, prefix, description, sort_order, is_active)
                        VALUES (:code, :name, :prefix, :desc, :sort, TRUE)
                    """),
                    {"code": code, "name": cat_name, "prefix": prefix, "desc": desc, "sort": created + 1},
                )
                print(f"  ✨ {cat_name} -> {prefix} (新建)")
                created += 1

        db.commit()
        print(f"\n✅ 完成！共建立 {created} 個新類別")

        # 顯示所有類別
        print(f"\n📋 目前所有類別:")
        all_cats = db.execute(
            text("SELECT code, name, prefix FROM asset_categories ORDER BY sort_order, code")
        ).all()
        for c in all_cats:
            count = db.execute(
                text("SELECT COUNT(*) FROM assets WHERE category = :cat"), {"cat": c[1]}
            ).scalar()
            print(f"  [{c[0]:5s}] {c[1]:8s}  前綴: {c[2]:5s}  編號範例: {c[2]}26000001  ({count}件)")

    except Exception as e:
        db.rollback()
        print(f"❌ 錯誤: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    main()
