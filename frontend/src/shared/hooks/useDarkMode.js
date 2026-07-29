import { useState, useEffect } from 'react'

const STORAGE_KEY = 'wordle-solver-theme'

// Returns the OS preference as 'light' | 'dark'
function getSystemTheme() {
  return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light'
}

function getStoredTheme() {
  return localStorage.getItem(STORAGE_KEY) ?? 'system'
}

// Resolves the active theme from the stored preference
function resolveTheme(stored) {
  return stored === 'system' ? getSystemTheme() : stored
}

export function useTheme() {
  const [theme, setTheme] = useState(getStoredTheme)

  useEffect(() => {
    const active = resolveTheme(theme)
    document.documentElement.classList.toggle('dark', active === 'dark')
    document.documentElement.classList.toggle('light', active === 'light')
    localStorage.setItem(STORAGE_KEY, theme)
  }, [theme])

  // Keep 'system' in sync when OS preference changes
  useEffect(() => {
    const mq = window.matchMedia('(prefers-color-scheme: dark)')
    function onSystemChange() {
      setTheme(t => {
        if (t === 'system') {
          // Re-trigger the class update by returning the same value via a fresh state set
          const active = getSystemTheme()
          document.documentElement.classList.toggle('dark', active === 'dark')
          document.documentElement.classList.toggle('light', active === 'light')
        }
        return t
      })
    }
    mq.addEventListener('change', onSystemChange)
    return () => mq.removeEventListener('change', onSystemChange)
  }, [])

  return [theme, setTheme]
}
