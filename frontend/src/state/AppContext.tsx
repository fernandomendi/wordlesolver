import { createContext, useContext, useState } from 'react'
import type { Language } from '@/types'

// ── AppContext ─────────────────────────────────────────────────────────────────
// Owns app-wide settings shared across features.
// Currently: language and debug toggle.
// Extend here when a second feature needs shared state.

const DEBUG_KEY = 'wordle-solver-debug'

interface AppContextValue {
  language: Language
  setLanguage: (lang: Language) => void
  showDebug: boolean
  toggleDebug: () => void
}

const AppContext = createContext<AppContextValue | null>(null)

// ── AppProvider ────────────────────────────────────────────────────────────────

export function AppProvider({ children }: { children: React.ReactNode }) {
  const [language, setLanguageState] = useState<Language>(
    () => (localStorage.getItem('app-language') as Language) ?? 'es'
  )
  const [showDebug, setShowDebug] = useState(
    () => localStorage.getItem(DEBUG_KEY) === 'true'
  )

  function setLanguage(lang: Language) {
    localStorage.setItem('app-language', lang)
    setLanguageState(lang)
  }

  function toggleDebug() {
    setShowDebug(v => {
      localStorage.setItem(DEBUG_KEY, String(!v))
      return !v
    })
  }

  return (
    <AppContext.Provider value={{ language, setLanguage, showDebug, toggleDebug }}>
      {children}
    </AppContext.Provider>
  )
}

// ── useApp ─────────────────────────────────────────────────────────────────────

export function useApp(): AppContextValue {
  const ctx = useContext(AppContext)
  if (!ctx) throw new Error('useApp must be used inside <AppProvider>')
  return ctx
}
