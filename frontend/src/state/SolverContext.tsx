import { createContext, useContext, useReducer, useEffect } from 'react'
import type { Dispatch } from 'react'
import { solverReducer, INITIAL_STATE, ACTIONS, historyToSteps, isDraftValid, FEEDBACK } from './solverReducer'
import { useApp } from './AppContext'
import { solveWordle } from '@/api/client'
import { useConfetti } from '@/features/solver/hooks/useConfetti'
import type { SolverState, SolverAction, Language } from '@/types'

// ── SolverContext ──────────────────────────────────────────────────────────────
// Owns all solver game state. Must be nested inside <AppProvider>.
//
// Components call useSolver() to read state and trigger actions.
// Language change functions are exposed as typed helpers — components never
// dispatch raw action types for language changes.

interface SolverContextValue {
  state: SolverState
  dispatch: Dispatch<SolverAction>
  submitGuesses: () => Promise<void>
  requestLanguageChange: (lang: Language) => void
  confirmLanguageChange: () => void
  cancelLanguageChange: () => void
}

const SolverContext = createContext<SolverContextValue | null>(null)

// ── SolverProvider ─────────────────────────────────────────────────────────────

export function SolverProvider({ children }: { children: React.ReactNode }) {
  const { language, setLanguage } = useApp()
  const [state, dispatch] = useReducer(solverReducer, INITIAL_STATE)
  const { fire: fireConfetti } = useConfetti()

  // Fetch opening suggestion on mount, and again whenever the session resets
  // (sessionId increments on every RESET_ALL) or language changes.
  useEffect(() => {
    async function fetchOpening() {
      dispatch({ type: ACTIONS.SUBMIT_START })
      try {
        const result = await solveWordle({ language, steps: [] })
        dispatch({ type: ACTIONS.SUBMIT_SUCCESS, result, isWin: false })
        result.best_guess?.split('').forEach((char, i) => {
          dispatch({ type: ACTIONS.SET_GUESS_CHAR, index: i, char })
        })
      } catch {
        dispatch({ type: ACTIONS.SUBMIT_ERROR, message: null })
      }
    }
    fetchOpening()
  }, [state.sessionId, language]) // eslint-disable-line react-hooks/exhaustive-deps

  async function submitGuesses() {
    if (!isDraftValid(state.draftCells, state.draftFeedback)) return
    if (state.isSubmitting) return

    const nextHistory = [
      ...state.history,
      { cells: [...state.draftCells], feedback: [...state.draftFeedback] },
    ]
    const steps = historyToSteps(nextHistory)
    const isWin = state.draftFeedback.every(f => f === FEEDBACK.CORRECT)

    dispatch({ type: ACTIONS.SUBMIT_START })
    try {
      const result = await solveWordle({ language, steps })
      dispatch({ type: ACTIONS.ADD_STEP_FROM_DRAFT })
      dispatch({ type: ACTIONS.SUBMIT_SUCCESS, result, isWin })
      if (isWin) {
        fireConfetti()
      } else if (result.best_guess) {
        result.best_guess.split('').forEach((char, i) => {
          dispatch({ type: ACTIONS.SET_GUESS_CHAR, index: i, char })
        })
      }
    } catch (err: unknown) {
      dispatch({ type: ACTIONS.SUBMIT_ERROR, message: err instanceof Error ? err.message : null })
    }
  }

  // Language change helpers — components call these instead of dispatching directly.

  function requestLanguageChange(lang: Language) {
    if (lang === language) return
    if (state.history.length > 0) {
      // User has submitted rows — show confirm dialog before resetting
      dispatch({ type: ACTIONS.SHOW_LANGUAGE_CONFIRM, language: lang })
    } else {
      // No history — switch immediately and reset the solver session
      setLanguage(lang)
      dispatch({ type: ACTIONS.RESET_ALL })
    }
  }

  function confirmLanguageChange() {
    if (!state.pendingLanguage) return
    setLanguage(state.pendingLanguage)
    dispatch({ type: ACTIONS.HIDE_LANGUAGE_CONFIRM })
    dispatch({ type: ACTIONS.RESET_ALL })
  }

  function cancelLanguageChange() {
    dispatch({ type: ACTIONS.HIDE_LANGUAGE_CONFIRM })
  }

  return (
    <SolverContext.Provider value={{ state, dispatch, submitGuesses, requestLanguageChange, confirmLanguageChange, cancelLanguageChange }}>
      {children}
    </SolverContext.Provider>
  )
}

// ── useSolver ──────────────────────────────────────────────────────────────────
// Any component inside <SolverProvider> can call this to access solver state.

export function useSolver(): SolverContextValue {
  const ctx = useContext(SolverContext)
  if (!ctx) throw new Error('useSolver must be used inside <SolverProvider>')
  return ctx
}
