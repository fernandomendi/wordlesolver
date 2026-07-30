import { useSolver } from './state/SolverContext'
import { GuessGrid } from '@/features/solver/components/GuessGrid'
import { ErrorBanner } from '@/shared/ui/ErrorBanner'
import { BestGuessPanel } from '@/features/results/components/BestGuessPanel'
import { WordListPanel } from '@/features/results/components/WordListPanel'
import { LanguageResetConfirm } from '@/features/solver/components/LanguageResetConfirm'
import { DebugPane } from '@/shared/ui/DebugPane'
import { SettingsPane } from '@/shared/ui/SettingsPane'
import { NotificationStack } from '@/shared/ui/NotificationStack'

export default function App() {
  const { state, dispatch } = useSolver()

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
            <GuessGrid />
          </div>

          <BestGuessPanel />

          {state.gameOver && (
            <p className="mt-4 text-center text-sm font-bold text-slate-900 dark:text-zinc-100">
              {state.isWin ? '🎉 Solved!' : '😵 Better luck next time!'}
            </p>
          )}
        </section>

        {/* Right column: fixed width so skeleton↔content swap doesn't reflow layout */}
        <section className="mx-auto w-80 rounded-2xl border border-slate-200 bg-white p-8 shadow-sm dark:border-zinc-700 dark:bg-zinc-900 md:mx-0 md:shrink-0">
          <WordListPanel />
        </section>

      </div>

      <NotificationStack>
        <ErrorBanner />
      </NotificationStack>

      <SettingsPane />
      <DebugPane />
      <LanguageResetConfirm />
    </main>
  )
}

