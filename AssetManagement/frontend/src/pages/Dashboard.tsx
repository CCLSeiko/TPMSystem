import { useState, useEffect } from 'react'
import { Package, ClipboardList, Wrench, Users, AlertTriangle, CalendarClock } from 'lucide-react'
import { getStats } from '../api/dashboard'
import type { DashboardStats } from '../types'

export default function Dashboard() {
  const [stats, setStats] = useState<DashboardStats | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    getStats().then(setStats).catch(() => {}).finally(() => setLoading(false))
  }, [])

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64 text-gray-400">
        <div className="animate-spin w-8 h-8 border-4 border-blue-500 border-t-transparent rounded-full" />
      </div>
    )
  }

  const cards = [
    { label: '總資產數', value: stats?.total_assets ?? 0, icon: Package, color: 'text-blue-600', bg: 'bg-blue-50' },
    { label: '盤點紀錄', value: stats?.total_inventory_records ?? 0, icon: ClipboardList, color: 'text-orange-600', bg: 'bg-orange-50' },
    { label: '維護紀錄', value: stats?.total_maintenance_records ?? 0, icon: Wrench, color: 'text-green-600', bg: 'bg-green-50' },
    { label: '管理人員', value: stats?.total_staff ?? 0, icon: Users, color: 'text-purple-600', bg: 'bg-purple-50' },
  ]

  const statusColors: Record<string, string> = {
    '使用中': 'bg-green-100 text-green-700',
    '閒置': 'bg-yellow-100 text-yellow-700',
    '報廢': 'bg-red-100 text-red-700',
  }

  const categories = stats?.assets_by_category ?? {}
  const statuses = stats?.assets_by_status ?? {}

  return (
    <div>
      <h2 className="text-2xl font-bold text-gray-800 mb-6">儀表板</h2>

      {/* 統計卡片 */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        {cards.map((c) => (
          <div key={c.label} className="bg-white rounded-xl border border-gray-200 p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-500">{c.label}</p>
                <p className="text-3xl font-bold text-gray-800 mt-1">{c.value}</p>
              </div>
              <div className={`p-3 rounded-lg ${c.bg}`}>
                <c.icon className={`w-6 h-6 ${c.color}`} />
              </div>
            </div>
          </div>
        ))}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* 資產狀態分布 */}
        <div className="bg-white rounded-xl border border-gray-200 p-6">
          <h3 className="text-lg font-semibold text-gray-800 mb-4 flex items-center gap-2">
            <Package className="w-5 h-5 text-blue-500" /> 資產狀態分布
          </h3>
          {Object.entries(statuses).length === 0 ? (
            <p className="text-gray-400 text-sm">暫無資料</p>
          ) : (
            <div className="space-y-3">
              {Object.entries(statuses).map(([status, count]) => {
                const total = stats?.total_assets ?? 1
                const pct = ((count / total) * 100).toFixed(0)
                return (
                  <div key={status}>
                    <div className="flex justify-between text-sm mb-1">
                      <span className="text-gray-600">{status}</span>
                      <span className="font-medium">{count} 件 ({pct}%)</span>
                    </div>
                    <div className="w-full bg-gray-100 rounded-full h-2">
                      <div
                        className={`h-2 rounded-full ${status === '使用中' ? 'bg-green-500' : status === '閒置' ? 'bg-yellow-500' : 'bg-red-500'}`}
                        style={{ width: `${pct}%` }}
                      />
                    </div>
                  </div>
                )
              })}
            </div>
          )}
        </div>

        {/* 類別分布 & 預警 */}
        <div className="space-y-6">
          <div className="bg-white rounded-xl border border-gray-200 p-6">
            <h3 className="text-lg font-semibold text-gray-800 mb-4 flex items-center gap-2">
              <CalendarClock className="w-5 h-5 text-orange-500" /> 即將到來維護
            </h3>
            <p className="text-3xl font-bold text-orange-600">{stats?.upcoming_maintenance ?? 0}</p>
            <p className="text-sm text-gray-500 mt-1">30 天內需維護的設備</p>
          </div>

          <div className="bg-white rounded-xl border border-gray-200 p-6">
            <h3 className="text-lg font-semibold text-gray-800 mb-4 flex items-center gap-2">
              <AlertTriangle className="w-5 h-5 text-yellow-500" /> 最近盤點異常
            </h3>
            <p className="text-sm text-gray-500">前往「盤點管理」頁面查看異常項目</p>
          </div>
        </div>

        {/* 類別分布 */}
        <div className="bg-white rounded-xl border border-gray-200 p-6 lg:col-span-2">
          <h3 className="text-lg font-semibold text-gray-800 mb-4">資產類別統計</h3>
          {Object.entries(categories).length === 0 ? (
            <p className="text-gray-400 text-sm">暫無資料</p>
          ) : (
            <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-3">
              {Object.entries(categories)
                .sort(([, a], [, b]) => b - a)
                .map(([cat, count]) => (
                  <div key={cat} className="bg-gray-50 rounded-lg p-3 text-center">
                    <p className="text-lg font-bold text-gray-800">{count}</p>
                    <p className="text-xs text-gray-500 truncate">{cat}</p>
                  </div>
                ))}
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
