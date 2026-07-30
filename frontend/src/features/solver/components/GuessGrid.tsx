import { GuessRow } from './GuessRow'
import { FEEDBACK } from '@/state/solverReducer'
import { useSolver } from '@/state/SolverContext'
import type { FeedbackValue } from '@/types'

const TOTAL_ROWS = 6
const EMPTY_CELLS = ['', '', '', '', '']
const EMPTY_FEEDBACK: FeedbackValue[] = Array(5).fill(FEEDBACK.UNSET)

// GuessGrid renders all 6 rows and decides which one is active.
// It derives this purely from state — no extra state needed here.
export function GuessGrid() {
  const { state, dispatch, submitGuesses } = useSolver()
  const { history, draftCells, draftFeedback, gameOver, errorKey } = state
  const activeRow = history.length

  return (
    <div className="flex flex-col gap-1.5" aria-label="Guess grid">
      {Array.from({ length: TOTAL_ROWS }, (_, rowIndex) => {
        // Rows before the active row: locked submitted history
        if (rowIndex < activeRow) {
          return (
            <GuessRow
              key={rowIndex}
              cells={history[rowIndex].cells}
              feedback={history[rowIndex].feedback}
              isActive={false}
              dispatch={dispatch}
              onSubmit={submitGuesses}
            />
          )
        }

        // The active row: editable, connected to draft state
        if (rowIndex === activeRow && !gameOver) {
          return (
            <GuessRow
              key={rowIndex}
              cells={draftCells}
              feedback={draftFeedback}
              isActive={true}
              errorKey={errorKey}
              dispatch={dispatch}
              onSubmit={submitGuesses}
            />
          )
        }

        // Rows after the active row: empty placeholders
        return (
          <GuessRow
            key={rowIndex}
            cells={EMPTY_CELLS}
            feedback={EMPTY_FEEDBACK}
            isActive={false}
            dispatch={dispatch}
            onSubmit={submitGuesses}
          />
        )
      })}
    </div>
  )
}
