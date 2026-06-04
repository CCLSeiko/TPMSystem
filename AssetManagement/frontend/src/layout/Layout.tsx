import { Link, Outlet, useLocation } from 'react-router-dom'
import { Package, ClipboardList, Wrench, LayoutDashboard, Tags, QrCode } from 'lucide-react'

const navItems = [
  { path: '/', label: '儀表板', icon: LayoutDashboard },
  { path: '/assets', label: '資產台帳', icon: Package },
  { path: '/inventory', label: '盤點管理', icon: ClipboardList },
  { path: '/maintenance', label: '維修保養', icon: Wrench },
  { path: '/categories', label: '類別管理', icon: Tags },
  { path: '/qrcode', label: 'QR Code', icon: QrCode },
]

export default function Layout() {
  const location = useLocation()

  return (
    <div className="min-h-screen bg-gray-50 flex">
      {/* Sidebar */}
      <aside className="w-64 bg-white border-r border-gray-200">
        <div className="p-6">
          <h1 className="text-xl font-bold text-blue-600">資產管理系統</h1>
        </div>
        <nav className="px-4 space-y-1">
          {navItems.map((item) => {
            const isActive = location.pathname === item.path
            return (
              <Link
                key={item.path}
                to={item.path}
                className={`flex items-center gap-3 px-4 py-3 rounded-lg text-sm font-medium transition-colors ${
                  isActive
                    ? 'bg-blue-50 text-blue-700'
                    : 'text-gray-600 hover:bg-gray-50'
                }`}
              >
                <item.icon className="w-5 h-5" />
                {item.label}
              </Link>
            )
          })}
        </nav>
      </aside>

      {/* Main Content */}
      <main className="flex-1 p-8">
        <Outlet />
      </main>
    </div>
  )
}
