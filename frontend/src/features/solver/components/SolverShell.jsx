import { useSolver } from '../hooks/useSolver'
import { GuessGrid } from './GuessGrid'
import { ErrorBanner } from '@/shared/ui/ErrorBanner'
import { ResultPanel } from '@/features/results/components/ResultPanel'
import { LanguageSelector } from './LanguageSelector'
import { LanguageResetConfirm } from './LanguageResetConfirm'
import { DebugPane } from '@/shared/ui/DebugPane'
import { NotificationStack } from '@/shared/ui/NotificationStack'

export function SolverShell() {
  const { state, dispatch, submitGuesses } = useSolver()

  return (
    <main className="mx-auto flex min-h-screen w-full max-w-lg items-center justify-center px-6 py-16">
      <section className="w-full rounded-2xl border border-slate-200 bg-white p-8 shadow-sm">
        <div className="flex items-center justify-between">
          <div>
            <p className="text-sm font-medium uppercase tracking-wide text-emerald-700">Wordle Solver</p>
            <h1 className="mt-1 text-2xl font-semibold tracking-tight text-slate-900">Guess a word</h1>
          </div>
        <div className="flex items-center gap-2">
            <LanguageSelector language={state.language} dispatch={dispatch} />
            <button
              onClick={() => dispatch({ type: 'RESET_ALL' })}
              aria-label="Restart game"
              title="Restart"
              className="rounded-lg border border-slate-200 px-3 py-1.5 text-sm font-medium text-slate-500 hover:bg-slate-50 hover:text-slate-800"
            >
              ↺
            </button>
          </div>
        </div>

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

        <ResultPanel result={state.result} isSubmitting={state.isSubmitting} />

        {state.gameOver && (
          <p className="mt-4 text-center text-sm font-bold text-slate-900">
            {state.isWin ? '🎉 Solved!' : '😵 Better luck next time!'}
          </p>
        )}
      </section>

      <NotificationStack>
        {state.error && <ErrorBanner message={state.error} dispatch={dispatch} />}
      </NotificationStack>

      <DebugPane state={state} />

      <LanguageResetConfirm
        pendingLanguage={state.showLanguageResetConfirm ? state.pendingLanguage : null}
        dispatch={dispatch}
      />
    </main>
  )
}
