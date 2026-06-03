import { BrowserRouter, Routes, Route } from 'react-router-dom'
import Layout from './layout/Layout'
import Dashboard from './pages/Dashboard'
import AssetsList from './pages/AssetsList'
import InventoryList from './pages/InventoryList'
import MaintenanceList from './pages/MaintenanceList'
import CategoriesPage from './pages/CategoriesPage'

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Layout />}>
          <Route index element={<Dashboard />} />
          <Route path="assets" element={<AssetsList />} />
          <Route path="inventory" element={<InventoryList />} />
          <Route path="maintenance" element={<MaintenanceList />} />
          <Route path="categories" element={<CategoriesPage />} />
        </Route>
      </Routes>
    </BrowserRouter>
  )
}

export default App
