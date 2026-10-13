import { BrowserRouter } from 'react-router-dom'
import { ThemeProvider } from './context/ThemeContext'
import { AuthProvider } from './context/AuthContext'
import { CatMockTestProvider } from './context/CatMockTestContext'
import { CatPiProvider } from './context/CatPiContext'
import Navbar from './components/Navbar'
import LoginPromptModal from './components/auth/LoginPromptModal'
import AppRouter from './router'

function App() {
  return (
    <BrowserRouter>
      <ThemeProvider>
        <AuthProvider>
          <CatMockTestProvider>
            <CatPiProvider>
              <Navbar />
              <main>
                <AppRouter />
              </main>
              <LoginPromptModal />
            </CatPiProvider>
          </CatMockTestProvider>
        </AuthProvider>
      </ThemeProvider>
    </BrowserRouter>
  )
}

export default App
