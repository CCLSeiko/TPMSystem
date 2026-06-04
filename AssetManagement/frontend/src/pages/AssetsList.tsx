import { useState, useEffect } from 'react'
import { Search, Filter, Plus, Edit2, Trash2, X, QrCode, Download } from 'lucide-react'
import { listAssets, createAsset, updateAsset, deleteAsset } from '../api/assets'
import { listCategories, getNextCode } from '../api/categories'
import { getQRCodeImageUrl } from '../api/qrcode'
import type { Asset, AssetCategory } from '../types'

const statusColors: Record<string, string> = {
  '使用中': 'bg-green-100 text-green-700',
  '閒置': 'bg-yellow-100 text-yellow-700',
  '報廢': 'bg-red-100 text-red-700',
}

const emptyForm: Partial<Asset> = {
  asset_code: '', asset_name: '', category: '', brand: '', model: '',
  purchase_date: '', purchase_price: '', department: '', location: '', status: '使用中', notes: '', disposal_reason: '',
}

export default function AssetsList() {
  const [assets, setAssets] = useState<Asset[]>([])
  const [categories, setCategories] = useState<AssetCategory[]>([])
  const [loading, setLoading] = useState(true)
  const [filterCat, setFilterCat] = useState('')
  const [filterStatus, setFilterStatus] = useState('')
  const [search, setSearch] = useState('')
  const [showForm, setShowForm] = useState(false)
  const [editing, setEditing] = useState<Asset | null>(null)
  const [form, setForm] = useState<Partial<Asset>>(emptyForm)
  const [qrPreviewAsset, setQrPreviewAsset] = useState<Asset | null>(null)

  const load = () => {
    setLoading(true)
    listAssets({ category: filterCat || undefined, status: filterStatus || undefined })
      .then(setAssets).catch(() => {}).finally(() => setLoading(false))
    listCategories().then(setCategories).catch(() => {})
  }

  useEffect(() => { load() }, [filterCat, filterStatus])

  const filtered = assets.filter((a) =>
    !search || a.asset_code.includes(search) || a.asset_name.includes(search)
  )

  const catOptions = [...new Set(assets.map((a) => a.category).filter(Boolean))]

  const openNew = async () => {
    setEditing(null)
    if (categories.length > 0) {
      const first = categories[0]
      const code = await getNextCode(first.id).catch(() => ({ next_code: '' }))
      setForm({ ...emptyForm, category: first.name, asset_code: code.next_code })
    } else {
      setForm({ ...emptyForm })
    }
    setShowForm(true)
  }

  const openEdit = (asset: Asset) => {
    setEditing(asset)
    setForm({ ...asset })
    setShowForm(true)
  }

  const handleSave = async () => {
    if (editing) {
      await updateAsset(editing.id, form)
    } else {
      await createAsset(form)
    }
    setShowForm(false)
    load()
  }

  const handleDelete = async (id: number) => {
    if (!confirm('確定刪除此資產？')) return
    await deleteAsset(id)
    load()
  }

  return (
    <div>
      {/* 標題列 */}
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-2xl font-bold text-gray-800">資產台帳</h2>
        <button onClick={openNew} className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 text-sm font-medium flex items-center gap-2">
          <Plus className="w-4 h-4" /> 新增資產
        </button>
      </div>

      {/* 篩選列 */}
      <div className="bg-white rounded-xl border border-gray-200 p-4 mb-6 flex flex-wrap gap-4 items-center">
        <div className="flex items-center gap-2 flex-1 min-w-[200px]">
          <Search className="w-4 h-4 text-gray-400" />
          <input
            type="text" placeholder="搜尋資產編號或名稱..."
            className="border-0 outline-none text-sm flex-1"
            value={search} onChange={(e) => setSearch(e.target.value)}
          />
        </div>
        <div className="flex items-center gap-2">
          <Filter className="w-4 h-4 text-gray-400" />
          <select className="text-sm border border-gray-200 rounded-lg px-3 py-1.5 outline-none" value={filterCat} onChange={(e) => setFilterCat(e.target.value)}>
            <option value="">全部分類</option>
            {catOptions.map((c) => <option key={c!} value={c!}>{c}</option>)}
          </select>
          <select className="text-sm border border-gray-200 rounded-lg px-3 py-1.5 outline-none" value={filterStatus} onChange={(e) => setFilterStatus(e.target.value)}>
            <option value="">全部狀態</option>
            <option value="使用中">使用中</option>
            <option value="閒置">閒置</option>
            <option value="報廢">報廢</option>
          </select>
        </div>
      </div>

      {/* 表格 */}
      {loading ? (
        <div className="flex justify-center py-12">
          <div className="animate-spin w-8 h-8 border-4 border-blue-500 border-t-transparent rounded-full" />
        </div>
      ) : (
        <div className="bg-white rounded-xl border border-gray-200 overflow-hidden">
          <table className="w-full text-sm">
            <thead>
              <tr className="bg-gray-50 text-left text-gray-500">
                <th className="px-4 py-3 font-medium">編號</th>
                <th className="px-4 py-3 font-medium">名稱</th>
                <th className="px-4 py-3 font-medium">類別</th>
                <th className="px-4 py-3 font-medium">品牌</th>
                <th className="px-4 py-3 font-medium">部門</th>
                <th className="px-4 py-3 font-medium">位置</th>
                <th className="px-4 py-3 font-medium">購入金額</th>
                <th className="px-4 py-3 font-medium">狀態</th>
                <th className="px-4 py-3 font-medium">報廢原因</th>
                <th className="px-4 py-3 font-medium text-right">操作</th>
              </tr>
            </thead>
            <tbody>
              {filtered.map((a) => (
                <tr key={a.id} className="border-t border-gray-100 hover:bg-gray-50">
                  <td className="px-4 py-3 font-mono text-blue-600">{a.asset_code}</td>
                  <td className="px-4 py-3 text-gray-800">{a.asset_name}</td>
                  <td className="px-4 py-3 text-gray-600">{a.category}</td>
                  <td className="px-4 py-3 text-gray-600">{a.brand}</td>
                  <td className="px-4 py-3 text-gray-600">{a.department}</td>
                  <td className="px-4 py-3 text-gray-600">{a.location}</td>
                  <td className="px-4 py-3 text-gray-600">{a.purchase_price ? `$${a.purchase_price}` : '-'}</td>
                  <td className="px-4 py-3">
                    <span className={`px-2 py-0.5 rounded-full text-xs font-medium ${statusColors[a.status] || 'bg-gray-100 text-gray-600'}`}>
                      {a.status}
                    </span>
                  </td>
                  <td className="px-4 py-3 text-gray-500 text-xs max-w-[150px] truncate">
                    {a.status === '報廢' ? (a.disposal_reason || '-') : '-'}
                  </td>
                  <td className="px-4 py-3 text-right">
                    <button onClick={() => setQrPreviewAsset(a)} className="p-1 text-gray-400 hover:text-green-600" title="QR Code"><QrCode className="w-4 h-4" /></button>
                    <button onClick={() => openEdit(a)} className="p-1 text-gray-400 hover:text-blue-600"><Edit2 className="w-4 h-4" /></button>
                    <button onClick={() => handleDelete(a.id)} className="p-1 text-gray-400 hover:text-red-600 ml-1"><Trash2 className="w-4 h-4" /></button>
                  </td>
                </tr>
              ))}
              {filtered.length === 0 && (
                <tr><td colSpan={10} className="px-4 py-12 text-center text-gray-400">暫無資產資料</td></tr>
              )}
            </tbody>
          </table>
          <div className="px-4 py-3 border-t border-gray-100 text-sm text-gray-400">
            共 {filtered.length} 筆（篩選後）
          </div>
        </div>
      )}

      {/* 新增/編輯 Modal */}
      {showForm && (
        <div className="fixed inset-0 bg-black/30 flex items-center justify-center z-50" onClick={() => setShowForm(false)}>
          <div className="bg-white rounded-xl shadow-xl w-full max-w-lg mx-4 max-h-[80vh] overflow-y-auto" onClick={(e) => e.stopPropagation()}>
            <div className="flex items-center justify-between p-6 border-b border-gray-100">
              <h3 className="text-lg font-semibold">{editing ? '編輯資產' : '新增資產'}</h3>
              <button onClick={() => setShowForm(false)}><X className="w-5 h-5 text-gray-400" /></button>
            </div>
            <div className="p-6 space-y-4">
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="text-sm text-gray-500 block mb-1">資產編號 <span className="text-blue-500">(自動產生)</span></label>
                  <div className="flex items-center gap-2">
                    <input className="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm outline-none bg-gray-50 text-gray-500 font-mono" value={form.asset_code || ''} readOnly />
                  </div>
                </div>
                <div>
                  <label className="text-sm text-gray-500 block mb-1">狀態</label>
                  <select className="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm outline-none focus:border-blue-400" value={form.status || '使用中'} onChange={(e) => setForm({ ...form, status: e.target.value })}>
                    <option value="使用中">使用中</option>
                    <option value="閒置">閒置</option>
                    <option value="報廢">報廢</option>
                  </select>
                </div>
              </div>
              {form.status === '報廢' && (
                <div>
                  <label className="text-sm text-gray-500 block mb-1">報廢原因 *</label>
                  <textarea className="w-full border border-red-200 rounded-lg px-3 py-2 text-sm outline-none focus:border-red-400" rows={2}
                    value={form.disposal_reason || ''}
                    onChange={(e) => setForm({ ...form, disposal_reason: e.target.value })}
                    placeholder="請填寫報廢原因（如：設備老舊無法修復、已達使用年限...）" />
                </div>
              )}
              <div>
                <label className="text-sm text-gray-500 block mb-1">資產名稱 *</label>
                <input className="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm outline-none focus:border-blue-400" value={form.asset_name || ''} onChange={(e) => setForm({ ...form, asset_name: e.target.value })} />
              </div>
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="text-sm text-gray-500 block mb-1">類別</label>
                  <select
                    className="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm outline-none focus:border-blue-400"
                    value={form.category || ''}
                    onChange={async (e) => {
                      const catName = e.target.value
                      setForm({ ...form, category: catName })
                      // 根據類別自動產生資產編號
                      if (!editing) {
                        const matched = categories.find(c => c.name === catName)
                        if (matched) {
                          const code = await getNextCode(matched.id).catch(() => ({ next_code: '' }))
                          setForm(f => ({ ...f, category: catName, asset_code: code.next_code }))
                        }
                      }
                    }}
                    disabled={!!editing}
                  >
                    <option value="">選擇類別</option>
                    {categories.map((c) => (
                      <option key={c.id} value={c.name}>{c.name} ({c.prefix}{String(new Date().getFullYear()).slice(-2)}xxxxxx)</option>
                    ))}
                  </select>
                </div>
                <div>
                  <label className="text-sm text-gray-500 block mb-1">品牌</label>
                  <input className="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm outline-none focus:border-blue-400" value={form.brand || ''} onChange={(e) => setForm({ ...form, brand: e.target.value })} />
                </div>
              </div>
              <div>
                <label className="text-sm text-gray-500 block mb-1">型號/規格</label>
                <input className="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm outline-none focus:border-blue-400" value={form.model || ''} onChange={(e) => setForm({ ...form, model: e.target.value })} />
              </div>
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="text-sm text-gray-500 block mb-1">部門</label>
                  <input className="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm outline-none focus:border-blue-400" value={form.department || ''} onChange={(e) => setForm({ ...form, department: e.target.value })} />
                </div>
                <div>
                  <label className="text-sm text-gray-500 block mb-1">位置</label>
                  <input className="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm outline-none focus:border-blue-400" value={form.location || ''} onChange={(e) => setForm({ ...form, location: e.target.value })} />
                </div>
              </div>
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="text-sm text-gray-500 block mb-1">購入日期</label>
                  <input type="date" className="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm outline-none focus:border-blue-400" value={form.purchase_date || ''} onChange={(e) => setForm({ ...form, purchase_date: e.target.value })} />
                </div>
                <div>
                  <label className="text-sm text-gray-500 block mb-1">購入金額</label>
                  <input type="number" className="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm outline-none focus:border-blue-400" value={form.purchase_price || ''} onChange={(e) => setForm({ ...form, purchase_price: e.target.value })} />
                </div>
              </div>
              <div>
                <label className="text-sm text-gray-500 block mb-1">備註</label>
                <textarea className="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm outline-none focus:border-blue-400" rows={2} value={form.notes || ''} onChange={(e) => setForm({ ...form, notes: e.target.value })} />
              </div>
            </div>
            <div className="p-6 border-t border-gray-100 flex justify-end gap-3">
              <button onClick={() => setShowForm(false)} className="px-4 py-2 text-sm text-gray-600 border border-gray-200 rounded-lg hover:bg-gray-50">取消</button>
              <button onClick={handleSave} className="px-4 py-2 text-sm text-white bg-blue-600 rounded-lg hover:bg-blue-700">儲存</button>
            </div>
          </div>
        </div>
      )}
      {qrPreviewAsset && (
        <div
          className="fixed inset-0 bg-black/30 flex items-center justify-center z-50"
          onClick={() => setQrPreviewAsset(null)}
        >
          <div
            className="bg-white rounded-2xl shadow-2xl p-8 text-center"
            onClick={(e) => e.stopPropagation()}
          >
            <img
              src={getQRCodeImageUrl(qrPreviewAsset.id)}
              alt={`QR Code ${qrPreviewAsset.asset_code}`}
              className="w-56 h-56 mx-auto"
            />
            <div className="mt-4">
              <div className="font-mono text-lg text-blue-600">{qrPreviewAsset.asset_code}</div>
              <div className="text-gray-600 text-sm mt-1">{qrPreviewAsset.asset_name}</div>
              <div className="text-xs text-gray-400 mt-1">{qrPreviewAsset.category} · {qrPreviewAsset.department}</div>
            </div>
            <button
              onClick={() => {
                const a = document.createElement('a')
                a.href = getQRCodeImageUrl(qrPreviewAsset.id)
                a.download = `qrcode_${qrPreviewAsset.asset_code}.png`
                document.body.appendChild(a)
                a.click()
                document.body.removeChild(a)
              }}
              className="mt-4 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 text-sm flex items-center gap-2 mx-auto"
            >
              <Download className="w-4 h-4" /> 下載 QR Code
            </button>
          </div>
        </div>
      )}
    </div>
  )
}
