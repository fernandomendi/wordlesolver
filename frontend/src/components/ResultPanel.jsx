// ResultPanel shows the solver's response after a successful submit.
// Kept intentionally minimal for now — #47 will add the full ranked list.
export function ResultPanel({ result, isSubmitting }) {
  if (isSubmitting) {
    return (
      <div className="mt-6 rounded-lg bg-slate-50 border border-slate-200 px-4 py-3 text-sm text-slate-500 text-center">
        Solving…
      </div>
    )
  }

  if (!result) return null

  return (
    <div className="mt-6 rounded-lg bg-slate-50 border border-slate-200 px-4 py-3 text-sm text-slate-700">
      <div className="flex items-center justify-between">
        <span className="text-slate-500">Best guess</span>
        <span className="font-bold uppercase tracking-widest text-slate-900">
          {result.best_guess}
        </span>
      </div>
      <div className="mt-1 flex items-center justify-between">
        <span className="text-slate-500">Possible words</span>
        <span className="font-semibold text-slate-900">{result.total_possible}</span>
      </div>
    </div>
  )
}
