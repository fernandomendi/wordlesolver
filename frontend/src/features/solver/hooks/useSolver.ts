import { useReducer, useEffect } from 'react'
import type { Dispatch } from 'react'
import { solverReducer, INITIAL_STATE, ACTIONS, historyToSteps, isDraftValid, FEEDBACK } from './solverReducer'
import type { SolverAction, SolverState } from '@/types'
import { solveWordle } from '@/api/client'
import { useConfetti } from './useConfetti'

export function useSolver(): { state: SolverState; dispatch: Dispatch<SolverAction>; submitGuesses: () => Promise<void> } {
  const [state, dispatch] = useReducer(solverReducer, INITIAL_STATE)
  const { fire: fireConfetti } = useConfetti()

  // On mount: fetch the opening suggestion with an empty step list
  useEffect(() => {
    async function fetchOpening() {
      dispatch({ type: ACTIONS.SUBMIT_START })
      try {
        const result = await solveWordle({ language: state.language, steps: [] })
        dispatch({ type: ACTIONS.SUBMIT_SUCCESS, result, isWin: false })
        result.best_guess?.split('').forEach((char, i) => {
          dispatch({ type: ACTIONS.SET_GUESS_CHAR, index: i, char })
        })
      } catch {
        dispatch({ type: ACTIONS.SUBMIT_ERROR, message: null })
      }
    }
    fetchOpening()
  }, [state.sessionId, state.language]) // eslint-disable-line react-hooks/exhaustive-deps

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
      if (isWin) {
        fireConfetti()
      } else if (result.best_guess) {
        // Pre-fill the next draft row with the solver's best guess
        result.best_guess.split('').forEach((char, i) => {
          dispatch({ type: ACTIONS.SET_GUESS_CHAR, index: i, char })
        })
      }
    } catch (err: unknown) {
      dispatch({ type: ACTIONS.SUBMIT_ERROR, message: err instanceof Error ? err.message : null })
    }
  }

  return { state, dispatch, submitGuesses }
}
