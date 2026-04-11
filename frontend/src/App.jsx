import { BrowserRouter, Route, Routes } from 'react-router-dom'
import Home from './page/Home'
import Login from './page/Login'
import Admin from './page/Admin'
import NotFound from './page/NotFound'
import ProtectedRoute from './components/ProtectedRoute'

function App() {

  return (
    <BrowserRouter>
      <Routes>
        <Route path="/home" element={<Home />} />
        <Route path='/' element={<Login />} />
        <Route
          path='/admin'
          element={
            <ProtectedRoute allowedRoles={['admin']}>
              <Admin />
            </ProtectedRoute>
          }
        />
        {/* 권한 부족 시 튕길 명시적 not-found 라우트 */}
        <Route path='/not-found' element={<NotFound />} />
        {/* 허용되지 않은 모든 잘못된 진입점 처리 */}
        <Route path='*' element={<NotFound />} />
      </Routes>
    </BrowserRouter>
  )
}

export default App
