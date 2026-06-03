"""
資產管理系統 - Excel 資料匯入工具
將資產管理.xlsx 中的資料匯入 PostgreSQL

使用方式:
  docker compose exec backend python import_data.py /app/資產管理.xlsx
"""

import sys
import pandas as pd
from sqlalchemy import text
from database import SessionLocal

# Excel 欄位 → 資料庫欄位對應（依實際 Excel 欄位名稱）
SHEET_CONFIG = {
    "資產基本資料": {
        "table": "assets",
        "columns": {
            "資產編號": "asset_code",
            "資產名稱": "asset_name",
            "資產類別": "category",
            "品牌": "brand",
            "型號": "model",
            "購入日期": "purchase_date",
            "購入金額": "purchase_price",
            "使用部門": "department",
            "存放位置": "location",
            "使用狀態": "status",
            "備註": "notes",
        },
    },
    "盤點紀錄": {
        "table": "inventory_records",
        "columns": {
            "盤點日期": "inventory_date",
            "資產編號": "asset_code",
            "預期位置": "expected_location",
            "實際位置": "actual_location",
            "盤點狀態": "status",
            "盤點人員": "inventory_person",
            "異常說明": "exception_description",
            "處理結果": "exception_result",
        },
    },
    "維護紀錄": {
        "table": "maintenance_records",
        "columns": {
            "資產編號": "asset_code",
            "維護日期": "maintenance_date",
            "維護類型": "maintenance_type",
            "維護內容": "description",
            "維護廠商": "vendor",
            "維護費用": "cost",
            "負責人員": "person_in_charge",
            "下次維護日期": "next_maintenance_date",
            "備註": "notes",
        },
    },
    "管理人員資料": {
        "table": "staff",
        "columns": {
            "姓名": "name",
            "部門": "department",
            "職稱": "role",
            "聯絡電話": "phone",
            "電子郵件": "email",
            "負責區域": "responsible_area",
        },
    },
}


def main(filepath: str):
    print(f"📂 開始匯入: {filepath}")
    xls = pd.ExcelFile(filepath)
    print(f"📄 工作表: {xls.sheet_names}\n")

    db = SessionLocal()
    total = 0

    try:
        for sheet_name, config in SHEET_CONFIG.items():
            if sheet_name not in xls.sheet_names:
                print(f"  ⏭️  跳過 '{sheet_name}' (不存在)")
                continue

            table = config["table"]
            col_map = config["columns"]

            df = pd.read_excel(xls, sheet_name=sheet_name)
            print(f"  📋 '{sheet_name}' - {len(df)} 筆資料")

            # 只取有對應的欄位並重新命名
            existing = {k: v for k, v in col_map.items() if k in df.columns}
            sub = df[list(existing.keys())].rename(columns=existing)

            # 處理 NaN → None
            sub = sub.where(pd.notna(sub), None)

            # 特殊處理：規格併入 model
            if "規格" in df.columns and sheet_name == "資產基本資料":
                # 合併型號與規格
                specs = df["規格"].where(pd.notna(df["規格"]), None)
                for i in sub.index:
                    if i in specs.index and specs[i]:
                        old_model = sub.at[i, "model"] or ""
                        sub.at[i, "model"] = f"{old_model} / {specs[i]}".strip(" /")

            # 特殊處理：管理人員 role — 中文轉英文
            if table == "staff":
                role_map = {"管理員": "admin", "操作員": "operator", "查閱者": "viewer"}
                sub["role"] = sub["role"].map(role_map).fillna("operator")

            # 匯入
            rows = len(sub)
            if rows == 0:
                print(f"      沒有可匯入的資料")
                continue

            # 先清空該表（避免重複匯入時發生衝突）
            db.execute(text(f"DELETE FROM {table}"))

            for _, row in sub.iterrows():
                record = row.to_dict()
                record = {k: v for k, v in record.items() if v is not None}
                cols = ", ".join(record.keys())
                vals = ", ".join([f":{k}" for k in record.keys()])
                db.execute(text(f"INSERT INTO {table} ({cols}) VALUES ({vals})"), record)

            db.commit()
            print(f"      ✅ 匯入 {rows} 筆")
            total += rows
    except Exception as e:
        db.rollback()
        print(f"\n❌ 錯誤: {e}")
        raise
    finally:
        db.close()

    print(f"\n🎉 全部匯入完成！共 {total} 筆資料")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python import_data.py <path_to_excel_file>")
        sys.exit(1)
    main(sys.argv[1])
