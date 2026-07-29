import { useTheme } from '@/shared/hooks/useDarkMode'

export function ThemeSelector() {
  const [theme, setTheme] = useTheme()

  return (
    <select
      value={theme}
      onChange={e => setTheme(e.target.value)}
      aria-label="Theme"
      className="rounded-lg border border-slate-200 bg-white px-3 py-1.5 text-sm font-medium text-slate-700 focus:outline-none focus:ring-2 focus:ring-emerald-500 dark:border-zinc-600 dark:bg-zinc-800 dark:text-zinc-300"
    >
      <option value="system">System</option>
      <option value="light">Light</option>
      <option value="dark">Dark</option>
    </select>
  )
}
