import { useState, useEffect } from 'react'
import type { Dispatch, SetStateAction } from 'react'
import type { ThemePreference } from '@/types'

const STORAGE_KEY = 'wordle-solver-theme'

function getSystemTheme(): 'light' | 'dark' {
  return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light'
}

function getStoredTheme(): ThemePreference {
  return (localStorage.getItem(STORAGE_KEY) as ThemePreference) ?? 'system'
}

function resolveTheme(stored: ThemePreference): 'light' | 'dark' {
  return stored === 'system' ? getSystemTheme() : stored
}

export function useTheme(): [ThemePreference, Dispatch<SetStateAction<ThemePreference>>] {
  const [theme, setTheme] = useState<ThemePreference>(getStoredTheme)

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
