import { GuessRow } from './GuessRow'
import { FEEDBACK } from '../hooks/solverReducer'

const TOTAL_ROWS = 6
const EMPTY_CELLS = ['', '', '', '', '']
const EMPTY_FEEDBACK = Array(5).fill(FEEDBACK.UNSET)

// GuessGrid renders all 6 rows and decides which one is active.
// It derives this purely from state — no extra state needed here.
export function GuessGrid({ history, draftCells, draftFeedback, gameOver, dispatch, onSubmit }) {
  // The active row index is always the number of submitted rows.
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
              onSubmit={onSubmit}
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
              dispatch={dispatch}
              onSubmit={onSubmit}
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
            onSubmit={onSubmit}
          />
        )
      })}
    </div>
  )
}
