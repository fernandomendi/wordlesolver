import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App'
import { AppProvider } from './state/AppContext'
import { SolverProvider } from './state/SolverContext'

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <AppProvider>
      <SolverProvider>
        <App />
      </SolverProvider>
    </AppProvider>
  </StrictMode>,
)
