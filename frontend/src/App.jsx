import { BrowserRouter } from 'react-router-dom'
import { AuthProvider } from './context/AuthContext'
import { CatMockTestProvider } from './context/CatMockTestContext'
import Navbar from './components/Navbar'
import AppRouter from './router'

function App() {
  return (
    <BrowserRouter>
      <AuthProvider>
        <CatMockTestProvider>
          <Navbar />
          <main>
            <AppRouter />
          </main>
        </CatMockTestProvider>
      </AuthProvider>
    </BrowserRouter>
  )
}

export default App
