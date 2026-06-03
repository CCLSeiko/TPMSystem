import { useState, useEffect } from 'react'
import { AlertTriangle, Plus, X, CheckCircle, XCircle } from 'lucide-react'
import { listInventory, createInventory } from '../api/inventory'
import type { InventoryRecord } from '../types'

export default function InventoryList() {
  const [records, setRecords] = useState<InventoryRecord[]>([])
  const [loading, setLoading] = useState(true)
  const [filterStatus, setFilterStatus] = useState('')
  const [showForm, setShowForm] = useState(false)
  const [form, setForm] = useState<Partial<InventoryRecord>>({
    asset_code: '', inventory_date: new Date().toISOString().split('T')[0],
    inventory_person: '', expected_location: '', actual_location: '', status: '正常',
    exception_description: '', exception_result: '',
  })

  const load = () => {
    setLoading(true)
    listInventory({ status: filterStatus || undefined })
      .then(setRecords).catch(() => {}).finally(() => setLoading(false))
  }

  useEffect(() => { load() }, [filterStatus])

  const anomalous = records.filter((r) => r.status === '異常')

  const handleSave = async () => {
    // auto-detect position mismatch
    const locationMatch = form.actual_location === form.expected_location
    await createInventory({
      ...form,
      status: (!locationMatch && form.actual_location) ? '異常' : form.status,
    })
    setShowForm(false)
    load()
  }

  return (
    <div>
      {/* Header */}
      <div className="flex items-center justify-between mb-6">
        <div className="flex items-center gap-3">
          <h2 className="text-2xl font-bold text-gray-800">盤點管理</h2>
          {anomalous.length > 0 && (
            <span className="px-3 py-1 bg-red-50 text-red-600 text-sm rounded-full flex items-center gap-1">
              <AlertTriangle className="w-4 h-4" /> {anomalous.length} 項異常
            </span>
          )}
        </div>
        <button onClick={() => setShowForm(true)} className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 text-sm font-medium flex items-center gap-2">
          <Plus className="w-4 h-4" /> 建立盤點單
        </button>
      </div>

      {/* Filter */}
      <div className="bg-white rounded-xl border border-gray-200 p-4 mb-6 flex gap-4">
        <select className="text-sm border border-gray-200 rounded-lg px-3 py-1.5 outline-none" value={filterStatus} onChange={(e) => setFilterStatus(e.target.value)}>
          <option value="">全部狀態</option>
          <option value="正常">正常</option>
          <option value="異常">異常</option>
        </select>
        <span className="text-sm text-gray-400 self-center">共 {records.length} 筆紀錄</span>
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
                <th className="px-4 py-3 font-medium">盤點日期</th>
                <th className="px-4 py-3 font-medium">盤點人員</th>
                <th className="px-4 py-3 font-medium">預期位置</th>
                <th className="px-4 py-3 font-medium">實際位置</th>
                <th className="px-4 py-3 font-medium">狀態</th>
                <th className="px-4 py-3 font-medium">異常說明</th>
              </tr>
            </thead>
            <tbody>
              {records.map((r) => (
                <tr key={r.id} className={`border-t border-gray-100 ${r.status === '異常' ? 'bg-red-50' : 'hover:bg-gray-50'}`}>
                  <td className="px-4 py-3 font-mono text-blue-600">{r.asset_code}</td>
                  <td className="px-4 py-3 text-gray-800">{r.inventory_date}</td>
                  <td className="px-4 py-3 text-gray-600">{r.inventory_person}</td>
                  <td className="px-4 py-3 text-gray-600">{r.expected_location}</td>
                  <td className={`px-4 py-3 ${r.status === '異常' ? 'text-red-600 font-medium' : 'text-gray-600'}`}>
                    {r.actual_location}
                    {r.status === '異常' && <XCircle className="w-4 h-4 inline ml-1 text-red-500" />}
                  </td>
                  <td className="px-4 py-3">
                    <span className={`px-2 py-0.5 rounded-full text-xs font-medium ${r.status === '異常' ? 'bg-red-100 text-red-700' : 'bg-green-100 text-green-700'}`}>
                      {r.status}
                    </span>
                  </td>
                  <td className="px-4 py-3 text-gray-500 max-w-[200px] truncate">{r.exception_description || '-'}</td>
                </tr>
              ))}
              {records.length === 0 && (
                <tr><td colSpan={7} className="px-4 py-12 text-center text-gray-400">暫無盤點紀錄</td></tr>
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
              <h3 className="text-lg font-semibold">建立盤點單</h3>
              <button onClick={() => setShowForm(false)}><X className="w-5 h-5 text-gray-400" /></button>
            </div>
            <div className="p-6 space-y-4">
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="text-sm text-gray-500 block mb-1">資產編號 *</label>
                  <input className="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm outline-none focus:border-blue-400" value={form.asset_code || ''} onChange={(e) => setForm({ ...form, asset_code: e.target.value })} />
                </div>
                <div>
                  <label className="text-sm text-gray-500 block mb-1">盤點日期 *</label>
                  <input type="date" className="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm outline-none focus:border-blue-400" value={form.inventory_date || ''} onChange={(e) => setForm({ ...form, inventory_date: e.target.value })} />
                </div>
              </div>
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="text-sm text-gray-500 block mb-1">盤點人員</label>
                  <input className="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm outline-none focus:border-blue-400" value={form.inventory_person || ''} onChange={(e) => setForm({ ...form, inventory_person: e.target.value })} />
                </div>
                <div>
                  <label className="text-sm text-gray-500 block mb-1">狀態</label>
                  <select className="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm outline-none focus:border-blue-400" value={form.status || '正常'} onChange={(e) => setForm({ ...form, status: e.target.value })}>
                    <option value="正常">正常</option>
                    <option value="異常">異常</option>
                  </select>
                </div>
              </div>
              <div>
                <label className="text-sm text-gray-500 block mb-1">預期位置</label>
                <input className="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm outline-none focus:border-blue-400" value={form.expected_location || ''} onChange={(e) => setForm({ ...form, expected_location: e.target.value })} />
              </div>
              <div>
                <label className="text-sm text-gray-500 block mb-1">實際位置</label>
                <input className="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm outline-none focus:border-blue-400" value={form.actual_location || ''} onChange={(e) => setForm({ ...form, actual_location: e.target.value })} />
              </div>
              <div>
                <label className="text-sm text-gray-500 block mb-1">異常說明</label>
                <textarea className="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm outline-none focus:border-blue-400" rows={2} value={form.exception_description || ''} onChange={(e) => setForm({ ...form, exception_description: e.target.value })} />
              </div>
              <div>
                <label className="text-sm text-gray-500 block mb-1">處理結果</label>
                <textarea className="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm outline-none focus:border-blue-400" rows={2} value={form.exception_result || ''} onChange={(e) => setForm({ ...form, exception_result: e.target.value })} />
              </div>
            </div>
            <div className="p-6 border-t border-gray-100 flex justify-end gap-3">
              <button onClick={() => setShowForm(false)} className="px-4 py-2 text-sm text-gray-600 border border-gray-200 rounded-lg hover:bg-gray-50">取消</button>
              <button onClick={handleSave} className="px-4 py-2 text-sm text-white bg-blue-600 rounded-lg hover:bg-blue-700">儲存盤點</button>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
