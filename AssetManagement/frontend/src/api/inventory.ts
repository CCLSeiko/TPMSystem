import api from './client'
import type { InventoryRecord } from '../types'

export async function listInventory(params?: { asset_id?: number; status?: string }): Promise<InventoryRecord[]> {
  const { data } = await api.get('/inventory/', { params })
  return data
}

export async function createInventory(record: Partial<InventoryRecord>): Promise<InventoryRecord> {
  const { data } = await api.post('/inventory/', record)
  return data
}
