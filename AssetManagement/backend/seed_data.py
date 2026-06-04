"""
資產管理系統 - 資料初始化腳本
填入類別種子資料、預設管理員、測試資料
"""
from sqlalchemy import text
from database import SessionLocal


SEED_CATEGORIES = [
    ("COMP", "電腦設備", "COMP", "桌上型電腦、筆記型電腦、工作站", 1),
    ("SERV", "伺服器", "SERV", "機架式伺服器、刀鋒伺服器", 2),
    ("DISP", "顯示器", "DISP", "螢幕、顯示器、投影機", 3),
    ("PRNT", "印表機", "PRNT", "雷射印表機、噴墨印表機、多功能事務機", 4),
    ("MFP_", "多功能事務機", "MFP_", "影印/列印/掃描多功能機", 5),
    ("NETW", "網路設備", "NETW", "交換器、路由器、AP、防火牆", 6),
    ("STOR", "儲存設備", "STOR", "NAS、SAN、硬碟陣列", 7),
    ("POWR", "電源設備", "POWR", "UPS、穩壓器、電池", 8),
    ("FURN", "辦公傢俱", "FURN", "辦公桌、椅、櫃子", 9),
    ("HVAC", "空調設備", "HVAC", "冷氣、空調系統、通風設備", 10),
    ("MOBL", "行動裝置", "MOBL", "平板、手機、掃描槍", 11),
    ("AVEO", "影音設備", "AVEO", "喇叭、麥克風、攝影機、電話系統", 12),
    ("SECU", "門禁監控", "SECU", "門禁系統、監視器、警報器", 13),
]


def init_categories(db):
    count = db.query(type(db).__name__ != None).filter(text("1=0")).first()  # noop
    existing = db.execute(text("SELECT count(*) FROM asset_categories")).scalar()
    if existing and existing > 0:
        print(f"  ⏭️  類別已存在 ({existing} 筆)，跳過")
        return

    for code, name, prefix, desc, sort_order in SEED_CATEGORIES:
        db.execute(
            text(
                "INSERT INTO asset_categories (code, name, prefix, description, sort_order) "
                "VALUES (:code, :name, :prefix, :desc, :sort)"
            ),
            {"code": code, "name": name, "prefix": prefix, "desc": desc, "sort": sort_order},
        )
    db.commit()
    print(f"  ✅ 已匯入 {len(SEED_CATEGORIES)} 個類別")


def init_admin(db):
    existing = db.execute(text("SELECT count(*) FROM staff")).scalar()
    if existing and existing > 0:
        print(f"  ⏭️  人員已存在，跳過")
        return
    db.execute(
        text(
            "INSERT INTO staff (name, role, department, responsible_area) "
            "VALUES (:name, :role, :dept, :area)"
        ),
        {"name": "系統管理員", "role": "admin", "dept": "資訊部", "area": "全部"},
    )
    # 也用資產管理.xlsx 的管理人員
    db.execute(
        text(
            "INSERT INTO staff (name, role, department, responsible_area, phone, email) VALUES "
            "('王大明', 'admin', '資訊部', '總部大樓A區', '0912-345-678', 'wang@company.com'),"
            "('李小英', 'operator', '資訊部', '總部大樓B區', '0923-456-789', 'li@company.com'),"
            "('張經理', 'viewer', '財務部', '全部', '0934-567-890', 'zhang@company.com')"
        )
    )
    db.commit()
    print("  ✅ 已匯入管理人員")


if __name__ == "__main__":
    print("🔧 開始初始化資料庫種子資料...")
    db = SessionLocal()
    try:
        init_categories(db)
        init_admin(db)
        print("\n🎉 初始化完成！")
    except Exception as e:
        db.rollback()
        print(f"\n❌ 錯誤: {e}")
        raise
    finally:
        db.close()
