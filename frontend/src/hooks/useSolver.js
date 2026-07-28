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

    // Capture draft now — state is a snapshot and won't change during the async call
    const nextHistory = [
      ...state.history,
      { cells: [...state.draftCells], feedback: [...state.draftFeedback] },
    ]
    const steps = historyToSteps(nextHistory)

    dispatch({ type: ACTIONS.SUBMIT_START })
    try {
      const result = await solveWordle({ language: state.language, steps })
      // Lock the row only on success — keeps draft intact on API error
      dispatch({ type: ACTIONS.ADD_STEP_FROM_DRAFT })
      dispatch({ type: ACTIONS.SUBMIT_SUCCESS, result })
    } catch (err) {
      dispatch({ type: ACTIONS.SUBMIT_ERROR, message: err.message })
    }
  }

  return { state, dispatch, submitGuesses }
}
