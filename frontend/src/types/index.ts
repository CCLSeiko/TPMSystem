export interface Asset {
  id: number
  asset_code: string
  asset_name: string
  category: string | null
  brand: string | null
  model: string | null
  serial_number: string | null
  purchase_date: string | null
  purchase_price: string | null
  current_value: string | null
  department: string | null
  location: string | null
  custodian: string | null
  status: string
  notes: string | null
  disposal_reason: string | null
  created_at: string | null
  updated_at: string | null
}

export interface InventoryRecord {
  id: number
  asset_id: number | null
  asset_code: string
  inventory_date: string
  inventory_person: string | null
  expected_location: string | null
  actual_location: string | null
  location_match: boolean | null
  status: string
  exception_description: string | null
  exception_result: string | null
  notes: string | null
  created_at: string | null
}

export interface MaintenanceRecord {
  id: number
  asset_id: number | null
  asset_code: string
  maintenance_date: string
  maintenance_type: string | null
  description: string | null
  cost: string | null
  vendor: string | null
  person_in_charge: string | null
  next_maintenance_date: string | null
  notes: string | null
  created_at: string | null
}

export interface Staff {
  id: number
  name: string
  role: string
  department: string | null
  responsible_area: string | null
  phone: string | null
  email: string | null
  is_active: boolean | null
  created_at: string | null
}

export interface DashboardStats {
  total_assets: number
  total_inventory_records: number
  total_maintenance_records: number
  total_staff: number
  assets_by_status: Record<string, number>
  upcoming_maintenance: number
  assets_by_category: Record<string, number>
}

export interface AssetCategory {
  id: number
  code: string
  name: string
  prefix: string
  description: string | null
  sort_order: number
  is_active: boolean
  created_at: string | null
}
