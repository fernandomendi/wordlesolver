import { useSolver } from '@/hooks/useSolver'
import { GuessGrid } from '@/components/GuessGrid'

export function SolverShell() {
  const { state, dispatch, submitGuesses } = useSolver()

  return (
    <main className="mx-auto flex min-h-screen w-full max-w-lg items-center justify-center px-6 py-16">
      <section className="w-full rounded-2xl border border-slate-200 bg-white p-8 shadow-sm">
        <p className="text-sm font-medium uppercase tracking-wide text-emerald-700">Wordle Solver</p>
        <h1 className="mt-1 text-2xl font-semibold tracking-tight text-slate-900">Guess a word</h1>

        <div className="mt-6 flex justify-center">
          <GuessGrid
            history={state.history}
            draftCells={state.draftCells}
            draftFeedback={state.draftFeedback}
            gameOver={state.gameOver}
            dispatch={dispatch}
            onSubmit={submitGuesses}
          />
        </div>
      </section>
    </main>
  )
}
