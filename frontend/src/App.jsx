import { BrowserRouter } from 'react-router-dom'
import { AuthProvider } from './context/AuthContext'
import { CatMockTestProvider } from './context/CatMockTestContext'
import { CatPiProvider } from './context/CatPiContext'
import Navbar from './components/Navbar'
import AppRouter from './router'

function App() {
  return (
    <BrowserRouter>
      <AuthProvider>
        <CatMockTestProvider>
          <CatPiProvider>
            <Navbar />
            <main>
              <AppRouter />
            </main>
          </CatPiProvider>
        </CatMockTestProvider>
      </AuthProvider>
    </BrowserRouter>
  )
}

export default App
