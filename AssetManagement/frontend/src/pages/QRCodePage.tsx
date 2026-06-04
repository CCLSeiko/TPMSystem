import { useState, useEffect } from 'react'
import { QrCode, Download, Printer, Search } from 'lucide-react'
import { getQRCodePreview, getQRCodeImageUrl, getBatchDownloadUrl } from '../api/qrcode'
import type { QRCodeInfo } from '../api/qrcode'

const statusColors: Record<string, string> = {
  '使用中': 'bg-green-100 text-green-700',
  '閒置': 'bg-yellow-100 text-yellow-700',
  '報廢': 'bg-red-100 text-red-700',
}

export default function QRCodePage() {
  const [items, setItems] = useState<QRCodeInfo[]>([])
  const [loading, setLoading] = useState(true)
  const [search, setSearch] = useState('')
  const [previewId, setPreviewId] = useState<number | null>(null)

  useEffect(() => {
    getQRCodePreview()
      .then(setItems)
      .catch(() => {})
      .finally(() => setLoading(false))
  }, [])

  const filtered = items.filter((a) =>
    !search || a.asset_code.includes(search) || a.asset_name.includes(search)
  )

  const handlePrint = () => window.print()

  const handleDownload = () => {
    const a = document.createElement('a')
    a.href = getBatchDownloadUrl()
    a.download = 'qrcodes_all.zip'
    document.body.appendChild(a)
    a.click()
    document.body.removeChild(a)
  }

  return (
    <div>
      {/* 標題列 */}
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-2xl font-bold text-gray-800">QR Code 管理</h2>
        <div className="flex gap-2">
          <button
            onClick={handleDownload}
            className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 text-sm font-medium flex items-center gap-2"
          >
            <Download className="w-4 h-4" /> 下載全部 ZIP
          </button>
          <button
            onClick={handlePrint}
            className="px-4 py-2 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 text-sm font-medium flex items-center gap-2"
          >
            <Printer className="w-4 h-4" /> 列印全部
          </button>
        </div>
      </div>

      {/* 搜尋 */}
      <div className="bg-white rounded-xl border border-gray-200 p-4 mb-6">
        <div className="flex items-center gap-2 max-w-md">
          <Search className="w-4 h-4 text-gray-400" />
          <input
            type="text"
            placeholder="搜尋資產編號或名稱..."
            className="border-0 outline-none text-sm flex-1"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
          />
        </div>
      </div>

      {/* QR Code 網格 */}
      {loading ? (
        <div className="flex justify-center py-12">
          <div className="animate-spin w-8 h-8 border-4 border-blue-500 border-t-transparent rounded-full" />
        </div>
      ) : (
        <>
          <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-4 print:gap-3">
            {filtered.map((item) => (
              <div
                key={item.id}
                className="bg-white rounded-xl border border-gray-200 p-4 flex flex-col items-center hover:shadow-md transition-shadow print:shadow-none print:border-gray-300"
              >
                {/* QR Code 圖片 */}
                <img
                  src={getQRCodeImageUrl(item.id)}
                  alt={`QR Code ${item.asset_code}`}
                  className="w-32 h-32 cursor-pointer hover:opacity-80 transition-opacity"
                  onClick={() => setPreviewId(item.id)}
                />
                {/* 資產資訊 */}
                <div className="mt-3 text-center w-full">
                  <div className="text-xs font-mono text-blue-600 mb-0.5">{item.asset_code}</div>
                  <div className="text-xs text-gray-800 truncate w-full">{item.asset_name}</div>
                  <div className="flex items-center justify-center gap-2 mt-1">
                    <span className="text-xs text-gray-400">{item.category}</span>
                    <span className={`px-1.5 py-0.5 rounded-full text-[10px] font-medium ${statusColors[item.status] || 'bg-gray-100 text-gray-600'}`}>
                      {item.status}
                    </span>
                  </div>
                </div>
              </div>
            ))}
          </div>
          {filtered.length === 0 && (
            <div className="text-center py-12 text-gray-400">暫無符合的資產</div>
          )}
          <div className="mt-4 text-sm text-gray-400">
            共 {filtered.length} 筆 QR Code
          </div>
        </>
      )}

      {/* QR Code 放大 Modal */}
      {previewId !== null && (
        <div
          className="fixed inset-0 bg-black/40 flex items-center justify-center z-50"
          onClick={() => setPreviewId(null)}
        >
          <div
            className="bg-white rounded-2xl shadow-2xl p-8 text-center"
            onClick={(e) => e.stopPropagation()}
          >
            {(() => {
              const item = items.find((i) => i.id === previewId)
              return (
                <>
                  <img
                    src={getQRCodeImageUrl(previewId)}
                    alt="QR Code 放大"
                    className="w-56 h-56 mx-auto"
                  />
                  {item && (
                    <div className="mt-4">
                      <div className="font-mono text-lg text-blue-600">{item.asset_code}</div>
                      <div className="text-gray-600 text-sm mt-1">{item.asset_name}</div>
                      <a
                        href={item.qr_url}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="text-xs text-blue-500 underline mt-1 inline-block"
                      >
                        {item.qr_url}
                      </a>
                    </div>
                  )}
                  <button
                    onClick={() => {
                      const a = document.createElement('a')
                      a.href = getQRCodeImageUrl(previewId)
                      a.download = `qrcode_${item?.asset_code || previewId}.png`
                      document.body.appendChild(a)
                      a.click()
                      document.body.removeChild(a)
                    }}
                    className="mt-4 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 text-sm flex items-center gap-2 mx-auto"
                  >
                    <Download className="w-4 h-4" /> 下載此 QR Code
                  </button>
                </>
              )
            })()}
          </div>
        </div>
      )}
    </div>
  )
}
