import { useState, useEffect, useRef } from 'react'
import { historyToSteps } from '@/hooks/solverReducer'

export function DebugPane({ state }) {
  const [open, setOpen] = useState(false)
  const containerRef = useRef(null)

  // Close when clicking outside the container
  useEffect(() => {
    if (!open) return
    function handleClick(e) {
      if (!containerRef.current?.contains(e.target)) setOpen(false)
    }
    document.addEventListener('mousedown', handleClick)
    return () => document.removeEventListener('mousedown', handleClick)
  }, [open])

  if (import.meta.env.PROD) return null

  const payload = {
    language: state.language,
    steps: historyToSteps(state.history),
    draft: {
      cells: state.draftCells,
      feedback: state.draftFeedback,
    },
  }

  return (
    <div ref={containerRef} className="fixed bottom-4 right-4 z-50 text-xs">
      {open && (
        <div className="absolute bottom-11 right-0 w-80 rounded-lg border border-slate-200 bg-white shadow-xl">
          <p className="border-b border-slate-100 px-3 py-2 font-medium text-slate-500">Debug — API payload</p>
          <pre className="max-h-64 overflow-auto px-3 py-2 text-slate-700">
            {JSON.stringify(payload, null, 2)}
          </pre>
        </div>
      )}
      <button
        onClick={() => setOpen(o => !o)}
        aria-label="Toggle debug pane"
        className="flex h-9 w-9 items-center justify-center rounded-full border border-slate-200 bg-white text-base shadow-lg hover:bg-slate-50"
      >
        🐛
      </button>
    </div>
  )
}
