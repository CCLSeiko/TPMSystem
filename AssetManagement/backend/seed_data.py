"""
資產管理系統 - 資料初始化腳本
填入類別種子資料、預設管理員、測試資料
"""
from sqlalchemy import text
from database import SessionLocal
from core.auth import hash_password


SEED_CATEGORIES = [
    ("CMPT", "電腦設備", "CMPT", "桌上型電腦、筆記型電腦、工作站", 1),
    ("SERV", "伺服器", "SERV", "機架式伺服器、刀鋒伺服器", 2),
    ("DSPL", "顯示器", "DSPL", "螢幕、顯示器、投影機", 3),
    ("PRNT", "印表機", "PRNT", "雷射印表機、噴墨印表機、多功能事務機", 4),
    ("MULT", "多功能事務機", "MULT", "影印/列印/掃描多功能機", 5),
    ("NETW", "網路設備", "NETW", "交換器、路由器、AP、防火牆", 6),
    ("STGE", "儲存設備", "STGE", "NAS、SAN、硬碟陣列", 7),
    ("PWSU", "電源設備", "PWSU", "UPS、穩壓器、電池", 8),
    ("FURN", "辦公傢俱", "FURN", "辦公桌、椅、櫃子", 9),
    ("HVAC", "空調設備", "HVAC", "冷氣、空調系統、通風設備", 10),
    ("MBLE", "行動裝置", "MBLE", "平板、手機、掃描槍", 11),
    ("AVED", "影音設備", "AVED", "喇叭、麥克風、攝影機、電話系統", 12),
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

    # 建立預設管理員帳號
    admin_password = hash_password("admin123")
    db.execute(
        text(
            "INSERT INTO staff (name, username, password_hash, role, department, responsible_area) "
            "VALUES (:name, :username, :password_hash, :role, :dept, :area)"
        ),
        {
            "name": "系統管理員",
            "username": "admin",
            "password_hash": admin_password,
            "role": "admin",
            "dept": "資訊部",
            "area": "全部",
        },
    )

    # 建立測試帳號
    operator_password = hash_password("operator123")
    viewer_password = hash_password("viewer123")
    db.execute(
        text(
            "INSERT INTO staff (name, username, password_hash, role, department, responsible_area, phone, email) VALUES "
            "(:name1, :username1, :pwd1, 'operator', '資訊部', '總部大樓B區', '0923-456-789', 'operator@test.com'),"
            "(:name2, :username2, :pwd2, 'viewer', '財務部', '全部', '0934-567-890', 'viewer@test.com')"
        ),
        {
            "name1": "操作員",
            "username1": "operator",
            "pwd1": operator_password,
            "name2": "檢視者",
            "username2": "viewer",
            "pwd2": viewer_password,
        },
    )
    db.commit()
    print("  ✅ 已匯入管理人員（含帳號密碼）")
    print("     預設帳號：admin / admin123")
    print("     測試帳號：operator / operator123")
    print("     測試帳號：viewer / viewer123")


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
