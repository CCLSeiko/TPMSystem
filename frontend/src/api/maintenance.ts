import api from './client'
import type { MaintenanceRecord } from '../types'

export async function listMaintenance(params?: { asset_id?: number; maintenance_type?: string }): Promise<MaintenanceRecord[]> {
  const { data } = await api.get('/maintenance/', { params })
  return data
}

export async function createMaintenance(record: Partial<MaintenanceRecord>): Promise<MaintenanceRecord> {
  const { data } = await api.post('/maintenance/', record)
  return data
}
