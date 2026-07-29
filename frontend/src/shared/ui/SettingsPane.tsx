import { useState, useEffect, useRef } from 'react'
import type { Dispatch } from 'react'
import { ThemeSelector } from './ThemeSelector'
import { LanguageSelector } from '@/features/solver/components/LanguageSelector'
import type { Language, SolverAction } from '@/types'

interface SettingsPaneProps {
  language: Language
  dispatch: Dispatch<SolverAction>
  showDebug: boolean
  onToggleDebug: () => void
}

export function SettingsPane({ language, dispatch, showDebug, onToggleDebug }: SettingsPaneProps) {
  const [open, setOpen] = useState(false)
  const containerRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    if (!open) return
    function handleClick(e: MouseEvent) {
      if (!containerRef.current?.contains(e.target as Node)) setOpen(false)
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
            <label className="flex items-center justify-between gap-3 text-sm text-slate-600 dark:text-zinc-400">
              Debug panel
              <button
                role="switch"
                aria-checked={showDebug}
                onClick={onToggleDebug}
                className={[
                  'relative inline-flex h-5 w-9 shrink-0 cursor-pointer rounded-full border-2 border-transparent',
                  'transition-colors duration-200 focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:ring-offset-1',
                  showDebug ? 'bg-emerald-500' : 'bg-slate-200 dark:bg-zinc-600',
                ].join(' ')}
              >
                <span
                  className={[
                    'pointer-events-none inline-block h-4 w-4 rounded-full bg-white shadow',
                    'transition-transform duration-200',
                    showDebug ? 'translate-x-4' : 'translate-x-0',
                  ].join(' ')}
                />
              </button>
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
