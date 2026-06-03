import api from './client'
import type { Asset } from '../types'

export interface AssetQuery {
  category?: string
  status?: string
  department?: string
}

export async function listAssets(params?: AssetQuery): Promise<Asset[]> {
  const { data } = await api.get('/assets/', { params })
  return data
}

export async function getAsset(id: number): Promise<Asset> {
  const { data } = await api.get(`/assets/${id}`)
  return data
}

export async function createAsset(asset: Partial<Asset>): Promise<Asset> {
  const { data } = await api.post('/assets/', asset)
  return data
}

export async function updateAsset(id: number, asset: Partial<Asset>): Promise<Asset> {
  const { data } = await api.put(`/assets/${id}`, asset)
  return data
}

export async function deleteAsset(id: number): Promise<void> {
  await api.delete(`/assets/${id}`)
}
