import { useReducer } from 'react'
import { solverReducer, INITIAL_STATE, ACTIONS, historyToSteps, isDraftValid } from '@/hooks/solverReducer'
import { solveWordle } from '@/api/client'

// useSolver is the single point of contact between UI components and state.
// Components receive `state` (read-only snapshot) and `dispatch` (to fire actions).
// The async submit logic lives here because it spans two actions: START → SUCCESS/ERROR.
export function useSolver() {
  const [state, dispatch] = useReducer(solverReducer, INITIAL_STATE)

  async function submitGuesses() {
    if (!isDraftValid(state.draftCells, state.draftFeedback)) return
    if (state.isSubmitting) return

    // 1. Lock the draft row into history first
    dispatch({ type: ACTIONS.ADD_STEP_FROM_DRAFT })

    // 2. Build the full steps list including the row we just locked
    const nextHistory = [
      ...state.history,
      { cells: [...state.draftCells], feedback: [...state.draftFeedback] },
    ]
    const steps = historyToSteps(nextHistory)

    dispatch({ type: ACTIONS.SUBMIT_START })
    try {
      const result = await solveWordle({ language: state.language, steps })
      dispatch({ type: ACTIONS.SUBMIT_SUCCESS, result })
    } catch (err) {
      // Try to surface the API's JSON message; fall back to the raw error string
      let message = err.message
      try {
        const body = await err.response?.json()
        if (body?.message) message = body.message
      } catch {
        // ignore JSON parse failures
      }
      dispatch({ type: ACTIONS.SUBMIT_ERROR, message })
    }
  }

  return { state, dispatch, submitGuesses }
}
