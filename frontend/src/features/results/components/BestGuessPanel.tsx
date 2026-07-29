import type { SolverResult } from '@/types'

interface BestGuessPanelProps {
  result: SolverResult | null
  isSubmitting: boolean
}

export function BestGuessPanel({ result, isSubmitting }: BestGuessPanelProps) {
  return (
    <div className="mt-6 rounded-lg border border-slate-200 bg-slate-50 px-4 py-3 text-sm text-slate-700 dark:border-zinc-600 dark:bg-zinc-800 dark:text-zinc-300">
      <div className="flex items-center justify-between">
        <span className="text-slate-500 dark:text-zinc-400">Best guess</span>
        {isSubmitting
          ? <span className="h-4 w-16 animate-pulse rounded bg-slate-200 dark:bg-zinc-700" />
          : <span className="font-bold uppercase tracking-widest text-slate-900 dark:text-zinc-100">{result?.best_guess ?? '—'}</span>
        }
      </div>
    </div>
  )
}
