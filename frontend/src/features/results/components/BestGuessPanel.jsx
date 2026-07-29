export function BestGuessPanel({ result, isSubmitting }) {
  return (
    <div className="mt-6 rounded-lg border border-slate-200 bg-slate-50 px-4 py-3 text-sm text-slate-700">
      <div className="flex items-center justify-between">
        <span className="text-slate-500">Best guess</span>
        {isSubmitting
          ? <span className="h-4 w-16 animate-pulse rounded bg-slate-200" />
          : <span className="font-bold uppercase tracking-widest text-slate-900">{result?.best_guess ?? '—'}</span>
        }
      </div>
    </div>
  )
}
