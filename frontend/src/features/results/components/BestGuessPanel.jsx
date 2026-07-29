export function BestGuessPanel({ result, isSubmitting }) {
  return (
    <div className="mt-6 rounded-lg border border-slate-200 bg-slate-50 px-4 py-3 text-sm text-slate-700 dark:border-slate-600 dark:bg-slate-700 dark:text-slate-300">
      <div className="flex items-center justify-between">
        <span className="text-slate-500 dark:text-slate-400">Best guess</span>
        {isSubmitting
          ? <span className="h-4 w-16 animate-pulse rounded bg-slate-200 dark:bg-slate-600" />
          : <span className="font-bold uppercase tracking-widest text-slate-900 dark:text-slate-100">{result?.best_guess ?? '—'}</span>
        }
      </div>
    </div>
  )
}
