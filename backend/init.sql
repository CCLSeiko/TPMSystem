-- 資產管理系統 - 資料庫初始化腳本
-- 根據資產管理 Excel 四張表設計

-- =====================================================
-- 1. 管理人員資料表 (對應: 管理人員資料.xlsx)
-- =====================================================
CREATE TABLE IF NOT EXISTS staff (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    role VARCHAR(20) NOT NULL DEFAULT 'operator',  -- admin / operator / viewer
    department VARCHAR(100),
    responsible_area VARCHAR(200),
    phone VARCHAR(20),
    email VARCHAR(100),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =====================================================
-- 2. 資產基本資料表 (對應: 資產基本資料.xlsx)
-- =====================================================
CREATE TABLE IF NOT EXISTS assets (
    id SERIAL PRIMARY KEY,
    asset_code VARCHAR(20) UNIQUE NOT NULL,         -- 資產編號 (e.g. A0001)
    asset_name VARCHAR(200) NOT NULL,                -- 資產名稱
    category VARCHAR(100),                           -- 資產類別 (電腦/伺服器/辦公傢俱)
    brand VARCHAR(100),                              -- 品牌
    model VARCHAR(200),                              -- 型號/規格
    serial_number VARCHAR(100),                      -- 序號
    purchase_date DATE,                              -- 購入日期
    purchase_price DECIMAL(12, 2),                   -- 購入金額
    current_value DECIMAL(12, 2),                    -- 現值/折舊後價值
    department VARCHAR(100),                         -- 使用部門
    location VARCHAR(200),                           -- 存放位置
    custodian VARCHAR(50),                           -- 保管人
    status VARCHAR(20) DEFAULT '使用中',             -- 使用中 / 閒置 / 報廢
    notes TEXT,                                      -- 備註
    disposal_reason TEXT,                            -- 報廢原因
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =====================================================
-- 3. 盤點紀錄表 (對應: 盤點紀錄.xlsx)
-- =====================================================
CREATE TABLE IF NOT EXISTS inventory_records (
    id SERIAL PRIMARY KEY,
    asset_id INTEGER REFERENCES assets(id),
    asset_code VARCHAR(20) NOT NULL,
    inventory_date DATE NOT NULL,                    -- 盤點日期
    inventory_person VARCHAR(50),                    -- 盤點人員
    expected_location VARCHAR(200),                  -- 預期位置
    actual_location VARCHAR(200),                    -- 實際位置
    location_match BOOLEAN,                          -- 位置是否相符
    status VARCHAR(20) DEFAULT '正常',              -- 正常 / 異常
    exception_description TEXT,                      -- 異常說明
    exception_result TEXT,                           -- 處理結果
    notes TEXT,                                      -- 備註
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =====================================================
-- 4. 維護紀錄表 (對應: 維護紀錄.xlsx)
-- =====================================================
CREATE TABLE IF NOT EXISTS maintenance_records (
    id SERIAL PRIMARY KEY,
    asset_id INTEGER REFERENCES assets(id),
    asset_code VARCHAR(20) NOT NULL,
    maintenance_date DATE NOT NULL,                  -- 維護日期
    maintenance_type VARCHAR(50),                    -- 維修 / 保養 / 耗材更換
    description TEXT,                                -- 維護內容
    cost DECIMAL(12, 2) DEFAULT 0,                   -- 費用
    vendor VARCHAR(100),                             -- 維護廠商
    person_in_charge VARCHAR(50),                    -- 負責人
    next_maintenance_date DATE,                      -- 下次維護日期
    notes TEXT,                                      -- 備註
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =====================================================
-- 5. 資產類別資料表
-- =====================================================
CREATE TABLE IF NOT EXISTS asset_categories (
    id SERIAL PRIMARY KEY,
    code VARCHAR(20) UNIQUE NOT NULL,
    name VARCHAR(100) NOT NULL,
    prefix VARCHAR(10) NOT NULL,
    description TEXT,
    sort_order INTEGER DEFAULT 0,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 建立索引
CREATE INDEX idx_assets_code ON assets(asset_code);
CREATE INDEX idx_assets_category ON assets(category);
CREATE INDEX idx_assets_status ON assets(status);
CREATE INDEX idx_inventory_asset ON inventory_records(asset_id);
CREATE INDEX idx_maintenance_asset ON maintenance_records(asset_id);
CREATE INDEX idx_maintenance_next_date ON maintenance_records(next_maintenance_date);

-- 插入預設管理員
INSERT INTO staff (name, role, department, responsible_area)
VALUES ('系統管理員', 'admin', '資訊部', '全部')
ON CONFLICT DO NOTHING;
