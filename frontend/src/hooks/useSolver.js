import { useReducer } from 'react'
import { solverReducer, INITIAL_STATE, ACTIONS, historyToSteps, isDraftValid, FEEDBACK } from '@/hooks/solverReducer'
import { solveWordle } from '@/api/client'
import { useConfetti } from '@/hooks/useConfetti'

export function useSolver() {
  const [state, dispatch] = useReducer(solverReducer, INITIAL_STATE)
  const { fire: fireConfetti } = useConfetti()

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
      const result = await solveWordle({ language: state.language, steps })
      dispatch({ type: ACTIONS.ADD_STEP_FROM_DRAFT })
      dispatch({ type: ACTIONS.SUBMIT_SUCCESS, result, isWin })
      if (isWin) fireConfetti()
    } catch (err) {
      dispatch({ type: ACTIONS.SUBMIT_ERROR, message: err.message })
    }
  }

  return { state, dispatch, submitGuesses }
}
