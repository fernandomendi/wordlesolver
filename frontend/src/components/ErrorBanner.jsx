import { ACTIONS } from '@/hooks/solverReducer'

export function DismissButton({ onClick, colorClass = 'text-slate-300 hover:text-slate-500' }) {
  return (
    <button
      onClick={onClick}
      aria-label="Dismiss"
      className={`ml-auto shrink-0 rounded px-1 font-bold leading-none focus:outline-none focus:ring-2 focus:ring-current ${colorClass}`}
    >
      ✕
    </button>
  )
}

export function ErrorBanner({ message, dispatch }) {
  if (!message) return null

  function dismiss() {
    dispatch({ type: ACTIONS.DISMISS_ERROR })
  }

  function handleKeyDown(e) {
    if (e.key === 'Escape') dismiss()
  }

  return (
    <div
      role="alert"
      className="flex items-center gap-2 rounded-lg border border-red-200 bg-red-50 px-3 py-2 text-sm text-red-700 shadow-lg"
      onKeyDown={handleKeyDown}
    >
      <span className="grow">{message}</span>
      <DismissButton onClick={dismiss} colorClass="text-red-300 hover:text-red-600" />
    </div>
  )
}
