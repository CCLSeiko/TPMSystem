import { useState, useEffect } from 'react'
import { Plus, X, DollarSign, CalendarClock } from 'lucide-react'
import { listMaintenance, createMaintenance } from '../api/maintenance'
import type { MaintenanceRecord } from '../types'

const typeColors: Record<string, string> = {
  '故障維修': 'bg-red-100 text-red-700',
  '定期保養': 'bg-blue-100 text-blue-700',
  '耗材更換': 'bg-yellow-100 text-yellow-700',
}

export default function MaintenanceList() {
  const [records, setRecords] = useState<MaintenanceRecord[]>([])
  const [loading, setLoading] = useState(true)
  const [filterType, setFilterType] = useState('')
  const [showForm, setShowForm] = useState(false)
  const [form, setForm] = useState<Partial<MaintenanceRecord>>({
    asset_code: '', maintenance_date: new Date().toISOString().split('T')[0],
    maintenance_type: '定期保養', description: '', cost: '0',
    vendor: '', person_in_charge: '', next_maintenance_date: '', notes: '',
  })

  const load = () => {
    setLoading(true)
    listMaintenance({ maintenance_type: filterType || undefined })
      .then(setRecords).catch(() => {}).finally(() => setLoading(false))
  }

  useEffect(() => { load() }, [filterType])

  const totalCost = records.reduce((sum, r) => sum + (parseFloat(r.cost || '0')), 0)

  const handleSave = async () => {
    await createMaintenance(form)
    setShowForm(false)
    load()
  }

  return (
    <div>
      {/* Header */}
      <div className="flex items-center justify-between mb-6">
        <div className="flex items-center gap-3">
          <h2 className="text-2xl font-bold text-gray-800">維修保養</h2>
          <span className="px-3 py-1 bg-green-50 text-green-700 text-sm rounded-full flex items-center gap-1">
            <DollarSign className="w-4 h-4" /> 總費用: ${totalCost.toLocaleString()}
          </span>
        </div>
        <button onClick={() => setShowForm(true)} className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 text-sm font-medium flex items-center gap-2">
          <Plus className="w-4 h-4" /> 新增紀錄
        </button>
      </div>

      {/* Filter */}
      <div className="bg-white rounded-xl border border-gray-200 p-4 mb-6 flex gap-4 items-center">
        <select className="text-sm border border-gray-200 rounded-lg px-3 py-1.5 outline-none" value={filterType} onChange={(e) => setFilterType(e.target.value)}>
          <option value="">全部類型</option>
          <option value="故障維修">故障維修</option>
          <option value="定期保養">定期保養</option>
          <option value="耗材更換">耗材更換</option>
        </select>
        <span className="text-sm text-gray-400">共 {records.length} 筆紀錄</span>
      </div>

      {/* Table */}
      {loading ? (
        <div className="flex justify-center py-12">
          <div className="animate-spin w-8 h-8 border-4 border-blue-500 border-t-transparent rounded-full" />
        </div>
      ) : (
        <div className="bg-white rounded-xl border border-gray-200 overflow-hidden">
          <table className="w-full text-sm">
            <thead>
              <tr className="bg-gray-50 text-left text-gray-500">
                <th className="px-4 py-3 font-medium">資產編號</th>
                <th className="px-4 py-3 font-medium">維護日期</th>
                <th className="px-4 py-3 font-medium">類型</th>
                <th className="px-4 py-3 font-medium">維護內容</th>
                <th className="px-4 py-3 font-medium">廠商</th>
                <th className="px-4 py-3 font-medium">負責人</th>
                <th className="px-4 py-3 font-medium text-right">費用</th>
                <th className="px-4 py-3 font-medium">下次維護</th>
              </tr>
            </thead>
            <tbody>
              {records.map((r) => (
                <tr key={r.id} className="border-t border-gray-100 hover:bg-gray-50">
                  <td className="px-4 py-3 font-mono text-blue-600">{r.asset_code}</td>
                  <td className="px-4 py-3 text-gray-800">{r.maintenance_date}</td>
                  <td className="px-4 py-3">
                    <span className={`px-2 py-0.5 rounded-full text-xs font-medium ${typeColors[r.maintenance_type || ''] || 'bg-gray-100 text-gray-600'}`}>
                      {r.maintenance_type}
                    </span>
                  </td>
                  <td className="px-4 py-3 text-gray-600 max-w-[200px] truncate">{r.description || '-'}</td>
                  <td className="px-4 py-3 text-gray-600">{r.vendor || '-'}</td>
                  <td className="px-4 py-3 text-gray-600">{r.person_in_charge || '-'}</td>
                  <td className="px-4 py-3 text-right font-medium text-gray-800">
                    ${parseFloat(r.cost || '0').toLocaleString()}
                  </td>
                  <td className="px-4 py-3">
                    {r.next_maintenance_date ? (
                      <span className="flex items-center gap-1 text-gray-600">
                        <CalendarClock className="w-3 h-3" /> {r.next_maintenance_date}
                      </span>
                    ) : '-'}
                  </td>
                </tr>
              ))}
              {records.length === 0 && (
                <tr><td colSpan={8} className="px-4 py-12 text-center text-gray-400">暫無維護紀錄</td></tr>
              )}
            </tbody>
          </table>
        </div>
      )}

      {/* New Record Modal */}
      {showForm && (
        <div className="fixed inset-0 bg-black/30 flex items-center justify-center z-50" onClick={() => setShowForm(false)}>
          <div className="bg-white rounded-xl shadow-xl w-full max-w-lg mx-4" onClick={(e) => e.stopPropagation()}>
            <div className="flex items-center justify-between p-6 border-b border-gray-100">
              <h3 className="text-lg font-semibold">新增維護紀錄</h3>
              <button onClick={() => setShowForm(false)}><X className="w-5 h-5 text-gray-400" /></button>
            </div>
            <div className="p-6 space-y-4">
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="text-sm text-gray-500 block mb-1">資產編號 *</label>
                  <input className="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm outline-none focus:border-blue-400" value={form.asset_code || ''} onChange={(e) => setForm({ ...form, asset_code: e.target.value })} />
                </div>
                <div>
                  <label className="text-sm text-gray-500 block mb-1">維護日期 *</label>
                  <input type="date" className="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm outline-none focus:border-blue-400" value={form.maintenance_date || ''} onChange={(e) => setForm({ ...form, maintenance_date: e.target.value })} />
                </div>
              </div>
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="text-sm text-gray-500 block mb-1">維護類型</label>
                  <select className="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm outline-none focus:border-blue-400" value={form.maintenance_type || '定期保養'} onChange={(e) => setForm({ ...form, maintenance_type: e.target.value })}>
                    <option value="故障維修">故障維修</option>
                    <option value="定期保養">定期保養</option>
                    <option value="耗材更換">耗材更換</option>
                  </select>
                </div>
                <div>
                  <label className="text-sm text-gray-500 block mb-1">維護費用</label>
                  <input type="number" className="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm outline-none focus:border-blue-400" value={form.cost || '0'} onChange={(e) => setForm({ ...form, cost: e.target.value })} />
                </div>
              </div>
              <div>
                <label className="text-sm text-gray-500 block mb-1">維護內容</label>
                <textarea className="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm outline-none focus:border-blue-400" rows={2} value={form.description || ''} onChange={(e) => setForm({ ...form, description: e.target.value })} />
              </div>
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="text-sm text-gray-500 block mb-1">維護廠商</label>
                  <input className="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm outline-none focus:border-blue-400" value={form.vendor || ''} onChange={(e) => setForm({ ...form, vendor: e.target.value })} />
                </div>
                <div>
                  <label className="text-sm text-gray-500 block mb-1">負責人</label>
                  <input className="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm outline-none focus:border-blue-400" value={form.person_in_charge || ''} onChange={(e) => setForm({ ...form, person_in_charge: e.target.value })} />
                </div>
              </div>
              <div>
                <label className="text-sm text-gray-500 block mb-1">下次維護日期</label>
                <input type="date" className="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm outline-none focus:border-blue-400" value={form.next_maintenance_date || ''} onChange={(e) => setForm({ ...form, next_maintenance_date: e.target.value })} />
              </div>
              <div>
                <label className="text-sm text-gray-500 block mb-1">備註</label>
                <textarea className="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm outline-none focus:border-blue-400" rows={2} value={form.notes || ''} onChange={(e) => setForm({ ...form, notes: e.target.value })} />
              </div>
            </div>
            <div className="p-6 border-t border-gray-100 flex justify-end gap-3">
              <button onClick={() => setShowForm(false)} className="px-4 py-2 text-sm text-gray-600 border border-gray-200 rounded-lg hover:bg-gray-50">取消</button>
              <button onClick={handleSave} className="px-4 py-2 text-sm text-white bg-blue-600 rounded-lg hover:bg-blue-700">儲存維護</button>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
