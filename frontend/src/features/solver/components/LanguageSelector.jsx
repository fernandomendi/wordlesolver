import { ACTIONS } from '../hooks/solverReducer'

export function LanguageSelector({ language, dispatch }) {
  function handleChange(e) {
    const lang = e.target.value
    if (lang === language) return
    dispatch({ type: ACTIONS.REQUEST_LANGUAGE_CHANGE, language: lang })
  }

  return (
    <select
      value={language}
      onChange={handleChange}
      aria-label="Language"
      className="rounded-lg border border-slate-200 bg-white px-3 py-1.5 text-sm font-medium text-slate-700 focus:outline-none focus:ring-2 focus:ring-emerald-500 dark:border-slate-600 dark:bg-slate-700 dark:text-slate-300"
    >
      <option value="en">EN</option>
      <option value="es">ES</option>
    </select>
  )
}
