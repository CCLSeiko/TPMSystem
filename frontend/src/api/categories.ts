import api from './client'
import type { AssetCategory } from '../types'

export async function listCategories(): Promise<AssetCategory[]> {
  const { data } = await api.get('/categories/')
  return data
}

export async function getCategory(id: number): Promise<AssetCategory> {
  const { data } = await api.get(`/categories/${id}`)
  return data
}

export async function createCategory(cat: Partial<AssetCategory>): Promise<AssetCategory> {
  const { data } = await api.post('/categories/', cat)
  return data
}

export async function updateCategory(id: number, cat: Partial<AssetCategory>): Promise<AssetCategory> {
  const { data } = await api.put(`/categories/${id}`, cat)
  return data
}

export async function deleteCategory(id: number): Promise<void> {
  await api.delete(`/categories/${id}`)
}

export async function getNextCode(categoryId: number): Promise<{ prefix: string; next_code: string; next_number: number }> {
  const { data } = await api.get(`/categories/${categoryId}/next-code`)
  return data
}
