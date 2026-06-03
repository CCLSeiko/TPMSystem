import { useState, useEffect } from 'react'
import { Plus, Edit2, Trash2, X, Tag } from 'lucide-react'
import { listCategories, createCategory, updateCategory, deleteCategory } from '../api/categories'
import type { AssetCategory } from '../types'

const emptyForm: Partial<AssetCategory> = {
  code: '', name: '', prefix: '',
  description: '', sort_order: 0, is_active: true,
}

export default function CategoriesPage() {
  const [cats, setCats] = useState<AssetCategory[]>([])
  const [loading, setLoading] = useState(true)
  const [showForm, setShowForm] = useState(false)
  const [editing, setEditing] = useState<AssetCategory | null>(null)
  const [form, setForm] = useState<Partial<AssetCategory>>(emptyForm)

  const load = () => {
    setLoading(true)
    listCategories().then(setCats).catch(() => {}).finally(() => setLoading(false))
  }

  useEffect(() => { load() }, [])

  const openNew = () => {
    setEditing(null)
    setForm({ ...emptyForm, sort_order: cats.length + 1 })
    setShowForm(true)
  }

  const openEdit = (cat: AssetCategory) => {
    setEditing(cat)
    setForm({ ...cat })
    setShowForm(true)
  }

  const handleSave = async () => {
    if (editing) {
      await updateCategory(editing.id, form)
    } else {
      await createCategory(form)
    }
    setShowForm(false)
    load()
  }

  const handleDelete = async (id: number) => {
    if (!confirm('確定刪除此類別？')) return
    await deleteCategory(id)
    load()
  }

  return (
    <div>
      {/* Header */}
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-2xl font-bold text-gray-800">資產類別管理</h2>
        <button onClick={openNew} className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 text-sm font-medium flex items-center gap-2">
          <Plus className="w-4 h-4" /> 新增類別
        </button>
      </div>

      {/* 說明卡片 */}
      <div className="bg-blue-50 border border-blue-200 rounded-xl p-4 mb-6 text-sm text-blue-700">
        <strong>ⓘ 編號規則說明：</strong> 新增資產時，系統會根據所選類別的「編號前綴」+ 西元年自動產生 **12 碼** 資產編號（4 碼前綴 + 2 碼年份 + 6 碼流水號）。<br />
        例如類別「電腦設備」前綴 <code className="bg-blue-100 px-1 rounded">COMP</code>，今年為 <code className="bg-blue-100 px-1 rounded">{String(new Date().getFullYear()).slice(-2)}</code>，則新資產編號為 <code className="bg-blue-100 px-1 rounded">{`COMP${String(new Date().getFullYear()).slice(-2)}000001`}</code>、<code className="bg-blue-100 px-1 rounded">{`COMP${String(new Date().getFullYear()).slice(-2)}000002`}</code>...
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
                <th className="px-4 py-3 font-medium">排序</th>
                <th className="px-4 py-3 font-medium">代碼</th>
                <th className="px-4 py-3 font-medium">類別名稱</th>
                <th className="px-4 py-3 font-medium">編號前綴</th>
                <th className="px-4 py-3 font-medium">編號範例</th>
                <th className="px-4 py-3 font-medium">說明</th>
                <th className="px-4 py-3 font-medium">狀態</th>
                <th className="px-4 py-3 font-medium text-right">操作</th>
              </tr>
            </thead>
            <tbody>
              {cats.map((c) => (
                <tr key={c.id} className="border-t border-gray-100 hover:bg-gray-50">
                  <td className="px-4 py-3 text-gray-400 text-center">{c.sort_order}</td>
                  <td className="px-4 py-3 font-mono text-blue-600 font-medium">{c.code}</td>
                  <td className="px-4 py-3 text-gray-800">{c.name}</td>
                  <td className="px-4 py-3">
                    <span className="font-mono bg-gray-100 px-2 py-0.5 rounded text-blue-600 font-bold">{c.prefix}</span>
                  </td>
                  <td className="px-4 py-3 font-mono text-gray-500 text-xs">
                    {`${c.prefix}${String(new Date().getFullYear()).slice(-2)}000001`}
                  </td>
                  <td className="px-4 py-3 text-gray-500 max-w-[200px] truncate">{c.description || '-'}</td>
                  <td className="px-4 py-3">
                    <span className={`px-2 py-0.5 rounded-full text-xs font-medium ${c.is_active ? 'bg-green-100 text-green-700' : 'bg-gray-100 text-gray-500'}`}>
                      {c.is_active ? '啟用' : '停用'}
                    </span>
                  </td>
                  <td className="px-4 py-3 text-right">
                    <button onClick={() => openEdit(c)} className="p-1 text-gray-400 hover:text-blue-600"><Edit2 className="w-4 h-4" /></button>
                    <button onClick={() => handleDelete(c.id)} className="p-1 text-gray-400 hover:text-red-600 ml-1"><Trash2 className="w-4 h-4" /></button>
                  </td>
                </tr>
              ))}
              {cats.length === 0 && (
                <tr><td colSpan={8} className="px-4 py-12 text-center text-gray-400">尚無類別資料，請新增第一個類別</td></tr>
              )}
            </tbody>
          </table>
          <div className="px-4 py-3 border-t border-gray-100 text-sm text-gray-400">
            共 {cats.length} 個類別
          </div>
        </div>
      )}

      {/* Add/Edit Modal */}
      {showForm && (
        <div className="fixed inset-0 bg-black/30 flex items-center justify-center z-50" onClick={() => setShowForm(false)}>
          <div className="bg-white rounded-xl shadow-xl w-full max-w-md mx-4" onClick={(e) => e.stopPropagation()}>
            <div className="flex items-center justify-between p-6 border-b border-gray-100">
              <h3 className="text-lg font-semibold">{editing ? '編輯類別' : '新增類別'}</h3>
              <button onClick={() => setShowForm(false)}><X className="w-5 h-5 text-gray-400" /></button>
            </div>
            <div className="p-6 space-y-4">
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="text-sm text-gray-500 block mb-1">代碼 *</label>
                  <input className="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm outline-none focus:border-blue-400"
                    value={form.code || ''} onChange={(e) => setForm({ ...form, code: e.target.value })}
                    placeholder="PC" disabled={!!editing} />
                </div>
                <div>
                  <label className="text-sm text-gray-500 block mb-1">編號前綴 *</label>
                  <input className="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm outline-none focus:border-blue-400 font-mono"
                    value={form.prefix || ''} onChange={(e) => setForm({ ...form, prefix: e.target.value.toUpperCase() })}
                    placeholder="PC" />
                </div>
              </div>
              <div>
                <label className="text-sm text-gray-500 block mb-1">類別名稱 *</label>
                <input className="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm outline-none focus:border-blue-400"
                  value={form.name || ''} onChange={(e) => setForm({ ...form, name: e.target.value })}
                  placeholder="電腦設備" />
              </div>
              <div>
                <label className="text-sm text-gray-500 block mb-1">說明</label>
                <input className="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm outline-none focus:border-blue-400"
                  value={form.description || ''} onChange={(e) => setForm({ ...form, description: e.target.value })} />
              </div>
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="text-sm text-gray-500 block mb-1">排序</label>
                  <input type="number" className="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm outline-none focus:border-blue-400"
                    value={form.sort_order || 0} onChange={(e) => setForm({ ...form, sort_order: parseInt(e.target.value) || 0 })} />
                </div>
                <div>
                  <label className="text-sm text-gray-500 block mb-1">狀態</label>
                  <select className="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm outline-none focus:border-blue-400"
                    value={form.is_active ? 'true' : 'false'} onChange={(e) => setForm({ ...form, is_active: e.target.value === 'true' })}>
                    <option value="true">啟用</option>
                    <option value="false">停用</option>
                  </select>
                </div>
              </div>
            </div>
            <div className="p-6 border-t border-gray-100 flex justify-end gap-3">
              <button onClick={() => setShowForm(false)} className="px-4 py-2 text-sm text-gray-600 border border-gray-200 rounded-lg hover:bg-gray-50">取消</button>
              <button onClick={handleSave} className="px-4 py-2 text-sm text-white bg-blue-600 rounded-lg hover:bg-blue-700">儲存</button>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
