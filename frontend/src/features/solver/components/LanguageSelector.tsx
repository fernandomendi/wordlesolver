import { useSolver } from '@/state/SolverContext'
import { useApp } from '@/state/AppContext'

export function LanguageSelector() {
  const { language } = useApp()
  const { requestLanguageChange } = useSolver()

  function handleChange(e: React.ChangeEvent<HTMLSelectElement>) {
    const lang = e.target.value as import('@/types').Language
    requestLanguageChange(lang)
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
