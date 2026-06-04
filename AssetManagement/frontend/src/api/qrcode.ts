import api from './client'
import type { Asset } from '../types'

export interface QRCodeInfo {
  id: number
  asset_code: string
  asset_name: string
  category: string | null
  status: string
  qr_url: string
  qr_api: string
}

export async function getQRCodePreview(): Promise<QRCodeInfo[]> {
  const { data } = await api.get('/qrcode/batch/preview')
  return data
}

export function getQRCodeImageUrl(assetId: number): string {
  return `/api/qrcode/${assetId}`
}

export function getBatchDownloadUrl(): string {
  return '/api/qrcode/batch/download'
}
