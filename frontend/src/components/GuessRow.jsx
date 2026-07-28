import { useRef, useState, useEffect } from 'react'
import { GuessTile } from '@/components/GuessTile'
import { ACTIONS, isDraftValid } from '@/hooks/solverReducer'

// GuessRow owns keyboard interaction and focus management for one row.
// `useRef` lets us hold a reference to a DOM element across renders
// without causing a re-render when it changes — perfect for focus management.
export function GuessRow({ cells, feedback, isActive, dispatch, onSubmit }) {
  // Which cell index is currently focused (only meaningful when isActive)
  const [focusedCell, setFocusedCell] = useState(0)

  // An array of 5 refs, one per cell DOM element.
  // useRef(Array) gives us a stable container; we fill it in the `ref` prop below.
  const cellRefs = useRef([])

  // Move focus to a cell by index. Math.max/min clamp to 0–4.
  function focusCell(index) {
    const clamped = Math.max(0, Math.min(4, index))
    setFocusedCell(clamped)
    cellRefs.current[clamped]?.focus()  // ?. = only call if the element exists
  }

  // Auto-focus cell 0 when this row becomes the active row.
  // useEffect runs after render. The empty-ish dependency array [isActive] means
  // "re-run whenever isActive changes" — so it fires once when the row activates.
  useEffect(() => {
    if (isActive) focusCell(0)
  }, [isActive]) // eslint-disable-line react-hooks/exhaustive-deps

  
  const [showHint, setShowHint] = useState(false)

  function flashHint() {
    setShowHint(true)
    setTimeout(() => setShowHint(false), 1500)
  }

  function handleKeyDown(cellIndex, e) {
    if (!isActive) return

    // A–Z: write the letter into the cell, then advance focus right.
    if (/^[a-zA-Z]$/.test(e.key)) {
      e.preventDefault()
      dispatch({ type: ACTIONS.SET_GUESS_CHAR, index: cellIndex, char: e.key })
      // Stay on cell 4 once we reach the end (no wrap)
      if (cellIndex < 4) focusCell(cellIndex + 1)
      return
    }

    switch (e.key) {
      case 'ArrowLeft':
        e.preventDefault()
        focusCell(cellIndex - 1)
        break

      case 'ArrowRight':
        e.preventDefault()
        focusCell(cellIndex + 1)
        break

      // Space cycles the feedback status of the focused cell.
      case ' ':
        e.preventDefault()
        dispatch({ type: ACTIONS.CYCLE_FEEDBACK_AT, index: cellIndex })
        break

      // Backspace: clear this cell; if already empty, move left and clear that one.
      case 'Backspace':
        e.preventDefault()
        if (cells[cellIndex] !== '' || feedback[cellIndex] !== 'unset') {
          // Clear letter and colour on the current cell
          dispatch({ type: ACTIONS.SET_GUESS_CHAR, index: cellIndex, char: '' })
          dispatch({ type: ACTIONS.SET_FEEDBACK_AT, index: cellIndex, value: 'unset' })
        } else if (cellIndex > 0) {
          // Current cell already blank+unset — clear the one to the left
          dispatch({ type: ACTIONS.SET_GUESS_CHAR, index: cellIndex - 1, char: '' })
          dispatch({ type: ACTIONS.SET_FEEDBACK_AT, index: cellIndex - 1, value: 'unset' })
          focusCell(cellIndex - 1)
        }
        break

      case 'Enter':
        e.preventDefault()
        if (isDraftValid(cells, feedback)) {
          onSubmit()
        } else {
          flashHint()
        }
        break

      // ArrowUp / ArrowDown: intentionally ignored
      default:
        break
    }
  }

  // Track whether a cell was already focused *before* the click.
  // We must read this on mousedown — by the time onClick fires the browser
  // has already moved focus to the clicked element.
  const wasAlreadyFocused = useRef(false)

  function handleMouseDown(index) {
    wasAlreadyFocused.current = document.activeElement === cellRefs.current[index]
  }

  // Click: focus the tile on first click, cycle feedback only if already focused.
  function handleTileClick(index) {
    if (!isActive) return
    if (wasAlreadyFocused.current) {
      dispatch({ type: ACTIONS.CYCLE_FEEDBACK_AT, index })
    } else {
      focusCell(index)
    }
  }

  return (
    <div className="flex flex-col items-center gap-1">
      <div className="flex gap-1.5">
        {cells.map((letter, i) => (
          <GuessTile
            key={i}
            // Assign each element to its slot in the refs array.
            // Arrow function in `ref` is called with the DOM element when it mounts.
            ref={el => { cellRefs.current[i] = el }}
            letter={letter}
            feedback={feedback[i]}
            isActive={isActive}
            isFocused={isActive && focusedCell === i}
            onClick={() => handleTileClick(i)}
            onMouseDown={() => handleMouseDown(i)}
            onKeyDown={e => handleKeyDown(i, e)}
          />
        ))}
      </div>

      {/* Inline hint shown briefly when Enter is pressed on an incomplete row */}
      {showHint && (
        <p className="text-xs text-red-500" role="alert">
          Fill all 5 letters and set each tile colour first
        </p>
      )}
    </div>
  )
}
