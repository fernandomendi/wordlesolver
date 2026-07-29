import { useState, useEffect, useRef } from 'react'
import { ThemeSelector } from './ThemeSelector'
import { LanguageSelector } from '@/features/solver/components/LanguageSelector'

export function SettingsPane({ language, dispatch }) {
  const [open, setOpen] = useState(false)
  const containerRef = useRef(null)

  useEffect(() => {
    if (!open) return
    function handleClick(e) {
      if (!containerRef.current?.contains(e.target)) setOpen(false)
    }
    document.addEventListener('mousedown', handleClick)
    return () => document.removeEventListener('mousedown', handleClick)
  }, [open])

  return (
    <div ref={containerRef} className="fixed right-4 top-4 z-40 text-xs">
      {open && (
        <div className="absolute right-0 top-11 w-52 rounded-xl border border-slate-200 bg-white p-4 shadow-xl dark:border-zinc-700 dark:bg-zinc-900">
          <div className="flex flex-col gap-3">
            <label className="flex items-center justify-between gap-3 text-sm text-slate-600 dark:text-zinc-400">
              Theme
              <ThemeSelector />
            </label>
            <label className="flex items-center justify-between gap-3 text-sm text-slate-600 dark:text-zinc-400">
              Language
              <LanguageSelector language={language} dispatch={dispatch} />
            </label>
          </div>
        </div>
      )}
      <button
        onClick={() => setOpen(o => !o)}
        aria-label="Settings"
        title="Settings"
        className="flex h-9 w-9 items-center justify-center rounded-full border border-slate-200 bg-white text-base shadow-lg hover:bg-slate-50 dark:border-zinc-700 dark:bg-zinc-900 dark:hover:bg-zinc-800"
      >
        ⚙️
      </button>
    </div>
  )
}
