"""
產生 100 筆測試資產資料
"""

import random
from datetime import date, timedelta
from sqlalchemy import text
from database import SessionLocal

# ============ 資料池 ============
CATEGORIES = [
    ("電腦設備", ["Dell", "HP", "Lenovo", "ASUS"],
     ["OptiPlex 7090", "ProBook 450 G10", "ThinkCentre M75s", "ExpertCenter D5"]),
    ("螢幕", ["Dell", "LG", "Samsung", "ASUS"],
     ["U2723QE", "27UP850N", "S27A800", "ProArt PA278QV"]),
    ("伺服器", ["Dell", "HP", "Supermicro"],
     ["PowerEdge R750", "ProLiant DL380", "SYS-510T-M"]),
    ("網路設備", ["Cisco", "MikroTik", "Ubiquiti"],
     ["Catalyst 9200", "CRS326", "UniFi USW-Pro-24"]),
    ("印表機", ["HP", "Brother", "Epson"],
     ["LaserJet Pro M404", "HL-L2370DW", "WorkForce Pro WF-7920"]),
    ("辦公傢俱", ["IKEA", "Herman Miller", "Steelcase"],
     ["Bekant 升降桌", "Aeron 人體工學椅", "Gesture 辦公椅"]),
    ("空調設備", ["日立", "大金", "三菱電機"],
     ["RAS-50NF", "FTXV50SV", "MSZ-GE50VA"]),
    ("行動裝置", ["Apple", "Samsung", "ASUS"],
     ["iPad Pro M4", "Galaxy Tab S9", "ZenPad 3S"]),
    ("視聽設備", ["Epson", "Sony", "JBL"],
     ["EB-L730U", "WF-1000XM5", "Charge 5"]),
    ("安全設備", ["Hikvision", "Axis", "Dahua"],
     ["DS-2CD2386G2", "M3086-V", "IPC-HFW5842"]),
]

DEPARTMENTS = ["總務部", "資訊部", "人資部", "財務部", "業務部", "行銷部", "研發中心"]
LOCATIONS = [
    "總部大樓A區", "總部大樓B區", "研發中心", "業務大樓",
    "倉庫二樓", "會議中心", "員工休息區",
]
CUSTODIANS = ["王大明", "李小華", "張志偉", "陳美玲", "林建宏",
              "黃雅琪", "吳俊傑", "周雅婷", "鄭文彥", "許家豪"]
STATUSES = ["使用中", "使用中", "使用中", "使用中", "使用中", "使用中", "使用中", "閒置", "閒置", "報廢"]

SERIAL_BRAND = {
    "Dell": "SN-DELL-",
    "HP": "SN-HP-",
    "Lenovo": "SN-LNV-",
    "ASUS": "SN-ASUS-",
    "LG": "SN-LG-",
    "Samsung": "SN-SAM-",
    "IKEA": "SN-IKEA-",
    "Herman Miller": "SN-HM-",
    "Steelcase": "SN-STL-",
    "Cisco": "SN-CSC-",
    "MikroTik": "SN-MTK-",
    "Ubiquiti": "SN-UBI-",
    "Brother": "SN-BRO-",
    "Epson": "SN-EPS-",
    "Apple": "SN-APL-",
    "Supermicro": "SN-SPM-",
    "日立": "SN-HTC-",
    "大金": "SN-DAI-",
    "三菱電機": "SN-MIT-",
    "Hikvision": "SN-HIK-",
    "Axis": "SN-AXS-",
    "Dahua": "SN-DAH-",
    "Sony": "SN-SNY-",
    "JBL": "SN-JBL-",
}


def random_date(start_year=2020, end_year=2025):
    start = date(start_year, 1, 1)
    end = date(end_year, 12, 31)
    delta = (end - start).days
    return start + timedelta(days=random.randint(0, delta))


def generate_assets(count=100):
    assets = []
    used_codes = set()

    for i in range(count):
        # 選擇類別
        cat, brands, models = random.choice(CATEGORIES)
        brand = random.choice(brands)
        model = random.choice(models)
        purchase_date = random_date()
        purchase_price = random.choice([25000, 35000, 45000, 12000, 8000, 55000, 1500, 3000, 180000, 85000, 600, 2000])
        status = random.choice(STATUSES)

        # 折舊（直線法，5年折舊，殘值10%）
        years_held = (date.today() - purchase_date).days / 365.25
        if years_held >= 5:
            current_value = purchase_price * 0.1
        else:
            dep_rate = (1 - 0.1) / 5  # 每年折舊18%
            current_value = purchase_price * (1 - dep_rate * years_held)
        current_value = round(max(current_value, purchase_price * 0.1), 0)

        # 資產編號
        code_num = i + 1
        asset_code = f"T{code_num:04d}"
        while asset_code in used_codes:
            code_num += 1
            asset_code = f"T{code_num:04d}"
        used_codes.add(asset_code)

        serial_prefix = SERIAL_BRAND.get(brand, "SN-XXX-")
        serial_number = f"{serial_prefix}{random.randint(100000, 999999)}"

        notes_opts = [
            None, None, None, None, None,
            "2025年度新購", "部門調撥", "備用設備",
            "已過保固", "合約編號: SV-2025-001",
        ]

        assets.append({
            "asset_code": asset_code,
            "asset_name": f"{brand} {model}",
            "category": cat,
            "brand": brand,
            "model": model,
            "serial_number": serial_number,
            "purchase_date": purchase_date.isoformat(),
            "purchase_price": purchase_price,
            "current_value": current_value,
            "department": random.choice(DEPARTMENTS),
            "location": random.choice(LOCATIONS),
            "custodian": random.choice(CUSTODIANS),
            "status": status,
            "notes": random.choice(notes_opts),
        })

    return assets


def main():
    db = SessionLocal()
    try:
        count_before = db.execute(text("SELECT COUNT(*) FROM assets")).scalar()
        print(f"📊 目前資產總數: {count_before}")

        assets = generate_assets(100)
        print(f"📝 準備匯入 {len(assets)} 筆測試資料...")

        for i, a in enumerate(assets):
            db.execute(
                text("""
                    INSERT INTO assets
                        (asset_code, asset_name, category, brand, model,
                         serial_number, purchase_date, purchase_price, current_value,
                         department, location, custodian, status, notes)
                    VALUES
                        (:asset_code, :asset_name, :category, :brand, :model,
                         :serial_number, :purchase_date, :purchase_price, :current_value,
                         :department, :location, :custodian, :status, :notes)
                    ON CONFLICT (asset_code) DO NOTHING
                """),
                a,
            )
            if (i + 1) % 20 == 0:
                print(f"  進度: {i + 1}/{len(assets)}")

        db.commit()

        count_after = db.execute(text("SELECT COUNT(*) FROM assets")).scalar()
        print(f"\n✅ 匯入完成！資產總數: {count_before} → {count_after}")
        print(f"  新增: {count_after - count_before} 筆")

        # 顯示類別分布
        rows = db.execute(
            text("SELECT category, COUNT(*) as cnt FROM assets GROUP BY category ORDER BY cnt DESC")
        ).all()
        print(f"\n📋 類別分布:")
        for row in rows:
            print(f"  {row[0]}: {row[1]} 件")

    except Exception as e:
        db.rollback()
        print(f"\n❌ 錯誤: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    main()
