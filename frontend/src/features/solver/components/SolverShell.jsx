import { useState } from 'react'
import { useSolver } from '../hooks/useSolver'
import { GuessGrid } from './GuessGrid'
import { ErrorBanner } from '@/shared/ui/ErrorBanner'
import { BestGuessPanel } from '@/features/results/components/BestGuessPanel'
import { WordListPanel } from '@/features/results/components/WordListPanel'
import { LanguageResetConfirm } from './LanguageResetConfirm'
import { DebugPane } from '@/shared/ui/DebugPane'
import { SettingsPane } from '@/shared/ui/SettingsPane'
import { NotificationStack } from '@/shared/ui/NotificationStack'

const DEBUG_KEY = 'wordle-solver-debug'

export function SolverShell() {
  const { state, dispatch, submitGuesses } = useSolver()
  const [showDebug, setShowDebug] = useState(
    () => localStorage.getItem(DEBUG_KEY) === 'true'
  )

  function toggleDebug() {
    setShowDebug(v => {
      localStorage.setItem(DEBUG_KEY, !v)
      return !v
    })
  }

  return (
    <main className="mx-auto flex min-h-screen w-full max-w-fit items-center justify-center px-6 py-16">
      <div className="flex w-full flex-col gap-8 md:flex-row md:items-start md:gap-12">

        {/* Left column: grid + controls */}
        <section className="w-full rounded-2xl border border-slate-200 bg-white p-8 shadow-sm dark:border-zinc-700 dark:bg-zinc-900 md:max-w-sm md:shrink-0">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium uppercase tracking-wide text-emerald-700 dark:text-emerald-400">Wordle Solver</p>
              <h1 className="mt-1 text-2xl font-semibold tracking-tight text-slate-900 dark:text-zinc-100">Guess a word</h1>
            </div>
            <button
              onClick={() => dispatch({ type: 'RESET_ALL' })}
              aria-label="Restart game"
              title="Restart"
              className="rounded-lg border border-slate-200 px-3 py-1.5 text-sm font-medium text-slate-500 hover:bg-slate-50 hover:text-slate-800 dark:border-zinc-600 dark:text-zinc-400 dark:hover:bg-zinc-700 dark:hover:text-zinc-200"
            >
              ↺
            </button>
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

          <BestGuessPanel result={state.result} isSubmitting={state.isSubmitting} />

          {state.gameOver && (
            <p className="mt-4 text-center text-sm font-bold text-slate-900 dark:text-zinc-100">
              {state.isWin ? '🎉 Solved!' : '😵 Better luck next time!'}
            </p>
          )}
        </section>

        {/* Right column: word lists, sized to content */}
        <section className="rounded-2xl border border-slate-200 bg-white p-8 shadow-sm dark:border-zinc-700 dark:bg-zinc-900 md:shrink-0">
          <WordListPanel result={state.result} isLoading={state.isSubmitting} />
        </section>

      </div>

      <NotificationStack>
        {state.error && <ErrorBanner message={state.error} dispatch={dispatch} />}
      </NotificationStack>

      <SettingsPane
        language={state.language}
        dispatch={dispatch}
        showDebug={showDebug}
        onToggleDebug={toggleDebug}
      />
      <DebugPane state={state} visible={showDebug} />

      <LanguageResetConfirm
        pendingLanguage={state.showLanguageResetConfirm ? state.pendingLanguage : null}
        dispatch={dispatch}
      />
    </main>
  )
}
