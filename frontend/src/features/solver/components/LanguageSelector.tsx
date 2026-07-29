import type { Dispatch } from 'react'
import { ACTIONS } from '../hooks/solverReducer'
import type { Language, SolverAction } from '@/types'

interface LanguageSelectorProps {
  language: Language
  dispatch: Dispatch<SolverAction>
}

export function LanguageSelector({ language, dispatch }: LanguageSelectorProps) {
  function handleChange(e: React.ChangeEvent<HTMLSelectElement>) {
    const lang = e.target.value as Language
    if (lang === language) return
    dispatch({ type: ACTIONS.REQUEST_LANGUAGE_CHANGE, language: lang })
  }

  return (
    <select
      value={language}
      onChange={handleChange}
      aria-label="Language"
      className="rounded-lg border border-slate-200 bg-white px-3 py-1.5 text-sm font-medium text-slate-700 focus:outline-none focus:ring-2 focus:ring-emerald-500 dark:border-zinc-600 dark:bg-zinc-800 dark:text-zinc-300"
    >
      <option value="en">EN</option>
      <option value="es">ES</option>
    </select>
  )
}
