# TPM 固定資產管理系統 (TPM Asset Management System)

> **TPMSystem** — 一套完整的固定資產生命週期管理平台  
> 開發模式：Vibe Coding（AI 輔助開發）  
> 技術棧：Python FastAPI + React TypeScript + PostgreSQL

---

## 📋 系統架構概覽

```
┌─────────────────────────────────────────────────────────────┐
│                    使用者瀏覽器 (http://192.168.31.57)       │
├─────────────────────────────────────────────────────────────┤
│                    nginx 反向代理 (Port 80)                  │
│          / → 前端靜態檔    /api/ → 轉發後端 API              │
├──────────────────────────┬──────────────────────────────────┤
│   React SPA (TypeScript) │   FastAPI 後端 (Python)          │
│   ┌──────────────────┐   │   ┌──────────────────────────┐   │
│   │  儀表板           │   │   │  /api/assets/*           │   │
│   │  資產台帳列表/編輯 │   │   │  /api/inventory/*       │   │
│   │  盤點管理         │   │   │  /api/maintenance/*     │   │
│   │  維修保養         │   │   │  /api/staff/*           │   │
│   │  類別管理         │   │   │  /api/categories/*      │   │
│   │  API 通信 (axios) │   │   │  /api/stats (儀表板)    │   │
│   └──────────────────┘   │   └──────────────────────────┘   │
├──────────────────────────┴──────────────────────────────────┤
│                   PostgreSQL 資料庫 (Port 5432)              │
│   assets | inventory_records | maintenance_records |        │
│   staff | asset_categories                                  │
├─────────────────────────────────────────────────────────────┤
│                    Docker Compose 容器化                     │
│   ams-db (postgres:16) | ams-backend | ams-frontend        │
└─────────────────────────────────────────────────────────────┘
```

---

## 🏗️ 資料表結構（5 張表）

### 1. 資產基本資料表 (`assets`)
| 欄位 | 類型 | 說明 |
|:-----|:----:|:-----|
| id | SERIAL PK | 流水號 |
| asset_code | VARCHAR(20) UNIQUE | **資產編號**（12碼：4前綴+2年份+6流水號） |
| asset_name | VARCHAR(200) | 資產名稱 |
| category | VARCHAR(100) | 資產類別 |
| brand | VARCHAR(100) | 品牌 |
| model | VARCHAR(200) | 型號/規格 |
| serial_number | VARCHAR(100) | 序號 |
| purchase_date | DATE | 購入日期 |
| purchase_price | DECIMAL(12,2) | 購入金額 |
| current_value | DECIMAL(12,2) | 現值（折舊後） |
| department | VARCHAR(100) | 使用部門 |
| location | VARCHAR(200) | 存放位置 |
| custodian | VARCHAR(50) | 保管人 |
| status | VARCHAR(20) | **使用中 / 閒置 / 報廢** |
| notes | TEXT | 備註 |
| disposal_reason | TEXT | 報廢原因 |

### 2. 盤點紀錄表 (`inventory_records`)
| 欄位 | 類型 | 說明 |
|:-----|:----:|:-----|
| asset_code | VARCHAR(20) | 關聯資產編號 |
| inventory_date | DATE | 盤點日期 |
| inventory_person | VARCHAR(50) | 盤點人員 |
| expected_location | VARCHAR(200) | 預期位置 |
| actual_location | VARCHAR(200) | 實際位置 |
| status | VARCHAR(20) | **正常 / 異常** |
| exception_description | TEXT | 異常說明 |

### 3. 維護紀錄表 (`maintenance_records`)
| 欄位 | 類型 | 說明 |
|:-----|:----:|:-----|
| asset_code | VARCHAR(20) | 關聯資產編號 |
| maintenance_date | DATE | 維護日期 |
| maintenance_type | VARCHAR(50) | **故障維修 / 定期保養 / 耗材更換** |
| cost | DECIMAL(12,2) | 維護費用 |
| vendor | VARCHAR(100) | 維護廠商 |
| next_maintenance_date | DATE | 下次維護日期 |

### 4. 管理人員表 (`staff`)
| 欄位 | 類型 | 說明 |
|:-----|:----:|:-----|
| name | VARCHAR(50) | 姓名 |
| role | VARCHAR(20) | **admin / operator / viewer** |
| department | VARCHAR(100) | 部門 |
| responsible_area | VARCHAR(200) | 負責區域 |

### 5. 資產類別表 (`asset_categories`)
| 欄位 | 類型 | 說明 |
|:-----|:----:|:-----|
| code | VARCHAR(20) UNIQUE | 類別代碼（如 COMP） |
| name | VARCHAR(100) | 類別名稱（如 電腦設備） |
| prefix | VARCHAR(10) | **4 碼編號前綴** |
| sort_order | INTEGER | 排序順序 |

---

## 🧩 各類別編碼規則

| 類別 | 前綴 | 編號範例 |
|:-----|:----:|:--------:|
| 電腦設備 | COMP | COMP26000001 |
| 伺服器 | SERV | SERV26000001 |
| 螢幕 | DISP | DISP26000001 |
| 印表機 | PRNT | PRNT26000001 |
| 事務機 | MFP_ | MFP_26000001 |
| 網路設備 | NETW | NETW26000001 |
| 儲存設備 | STOR | STOR26000001 |
| 電源設備 | POWR | POWR26000001 |
| 辦公傢俱 | FURN | FURN26000001 |
| 空調設備 | HVAC | HVAC26000001 |
| 行動裝置 | MOBL | MOBL26000001 |
| 視聽設備 | AVEO | AVEO26000001 |
| 安全設備 | SECU | SECU26000001 |

---

## 🚀 快速啟動

```bash
# 啟動所有服務
cd ~/Develop/TPMSystem/Asset-Management-System
docker compose up -d --build

# 檢查狀態
docker compose ps

# 後端 API：http://localhost:8000/docs
# 前端網頁：http://localhost:3000
```

### 初始化類別資料
```bash
docker compose exec backend python seed_categories.py
```

### 匯入 Excel 資產資料
```bash
docker compose exec backend python import_data.py /app/資產管理.xlsx
```

---

## 📂 專案目錄結構

```
TPMSystem/
├── docker-compose.yml          # 容器編排（DB + Backend + Frontend）
├── backend/
│   ├── main.py                 # FastAPI 主程式 + 路由註冊
│   ├── database.py             # SQLAlchemy 連線設定
│   ├── models.py               # 資料表 ORM 模型
│   ├── schemas.py              # Pydantic 資料驗證
│   ├── init.sql                # 資料庫初始化腳本
│   ├── import_data.py          # Excel 資料匯入工具
│   ├── seed_categories.py      # 類別資料初始化
│   ├── generate_test_data.py   # 測試資料產生器
│   └── routers/
│       ├── assets.py           # 資產台帳 CRUD
│       ├── inventory.py        # 盤點管理 CRUD
│       ├── maintenance.py      # 維修保養 CRUD
│       ├── staff.py            # 人員管理 CRUD
│       ├── categories.py       # 類別管理 CRUD + 編號產生
│       └── dashboard.py        # 儀表板統計
└── frontend/
    ├── Dockerfile              # NGINX + React 多階段建置
    ├── nginx.conf              # 反向代理設定
    ├── src/
    │   ├── types/index.ts      # TypeScript 介面定義
    │   ├── api/                # API 通信層（axios）
    │   ├── layout/Layout.tsx   # 側邊欄導航
    │   └── pages/
    │       ├── Dashboard.tsx   # 儀表板（統計圖表）
    │       ├── AssetsList.tsx  # 資產台帳（列表/編輯）
    │       ├── InventoryList.tsx   # 盤點管理
    │       ├── MaintenanceList.tsx # 維修保養
    │       └── CategoriesPage.tsx  # 類別管理
```

---

## 💻 開發技術棧

| 層級 | 技術 | 用途 |
|:-----|:-----|:-----|
| 前端框架 | React 18 + TypeScript | SPA 應用 |
| 樣式 | Tailwind CSS 3 | UI 設計系統 |
| 圖標 | Lucide React | 介面圖標 |
| HTTP | Axios | API 通信 |
| 後端框架 | Python FastAPI | RESTful API |
| ORM | SQLAlchemy 2.0 | 資料庫操作 |
| 資料庫 | PostgreSQL 16 | 資料儲存 |
| 容器化 | Docker + Docker Compose | 環境部署 |

---

## 🔄 API 端點一覽

| 方法 | 路徑 | 說明 |
|:----:|:-----|:-----|
| GET | `/api/stats` | 儀表板統計 |
| GET/POST | `/api/assets/` | 資產列表 / 新增 |
| GET/PUT/DELETE | `/api/assets/{id}` | 資產詳情 / 更新 / 刪除 |
| GET/POST | `/api/inventory/` | 盤點列表 / 新增 |
| GET/POST | `/api/maintenance/` | 維護列表 / 新增 |
| GET/POST | `/api/categories/` | 類別列表 / 新增 |
| PUT/DELETE | `/api/categories/{id}` | 類別更新 / 刪除 |
| GET | `/api/categories/{id}/next-code` | 取得下一組資產編號 |
| GET/POST | `/api/staff/` | 人員列表 / 新增 |

---

## 📝 開發進度

- [x] **Phase 1** — 基礎地基（Docker + DB Schema + FastAPI + React）
- [x] **Phase 2** — 核心功能（四大模組 CRUD + 儀表板統計）
- [x] **Phase 2b** — 類別管理 + 12 碼資產編號自動產生（4+2+6）
- [x] **Phase 2c** — 報廢原因欄位
- [ ] **Phase 3** — QR Code 生成與掃描
- [ ] **Phase 3** — 資產折舊報表
- [ ] **Phase 3** — 自動維護提醒
- [ ] **Phase 4** — 雲端部署（GCP Cloud Run）
