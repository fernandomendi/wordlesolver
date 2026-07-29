import { ACTIONS } from '../hooks/solverReducer'

// Modal-style confirm dialog for language switch with unsaved progress.
// Rendered as a fixed overlay — same CSS technique as ErrorBanner.
export function LanguageResetConfirm({ pendingLanguage, dispatch }) {
  if (!pendingLanguage) return null

  function confirm() {
    dispatch({ type: ACTIONS.CONFIRM_LANGUAGE_CHANGE })
  }

  function cancel() {
    dispatch({ type: ACTIONS.CANCEL_LANGUAGE_CHANGE })
  }

  function handleKeyDown(e) {
    if (e.key === 'Escape') cancel()
  }

  return (
    // Semi-transparent backdrop covers the whole viewport
    <div
      className="fixed inset-0 z-50 flex items-center justify-center bg-black/30"
      onKeyDown={handleKeyDown}
      role="dialog"
      aria-modal="true"
      aria-labelledby="lang-confirm-title"
    >
      <div className="w-full max-w-sm rounded-2xl bg-white p-6 shadow-xl dark:bg-zinc-900">
        <h2 id="lang-confirm-title" className="text-base font-semibold text-slate-900 dark:text-zinc-100">
          Switch to {pendingLanguage.toUpperCase()}?
        </h2>
        <p className="mt-2 text-sm text-slate-600 dark:text-zinc-400">
          This will reset your current guesses and start a new game.
        </p>
        <div className="mt-5 flex justify-end gap-2">
          <button
            onClick={cancel}
            className="rounded-lg border border-slate-200 px-4 py-2 text-sm font-medium text-slate-600 hover:bg-slate-50 dark:border-zinc-600 dark:text-zinc-400 dark:hover:bg-zinc-700"
          >
            Cancel
          </button>
          <button
            autoFocus
            onClick={confirm}
            className="rounded-lg bg-emerald-600 px-4 py-2 text-sm font-medium text-white hover:bg-emerald-700"
          >
            Reset and switch
          </button>
        </div>
      </div>
    </div>
  )
}
