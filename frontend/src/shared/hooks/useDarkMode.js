import { useState, useEffect } from 'react'

const STORAGE_KEY = 'wordle-solver-dark-mode'

function getInitialDark() {
  const stored = localStorage.getItem(STORAGE_KEY)
  if (stored !== null) return stored === 'true'
  return window.matchMedia('(prefers-color-scheme: dark)').matches
}

export function useDarkMode() {
  const [isDark, setIsDark] = useState(getInitialDark)

  useEffect(() => {
    document.documentElement.classList.toggle('dark', isDark)
    localStorage.setItem(STORAGE_KEY, isDark)
  }, [isDark])

  return [isDark, () => setIsDark(d => !d)]
}
