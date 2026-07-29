import { useRef, useState, useEffect } from 'react'
import { GuessTile } from './GuessTile'
import { ACTIONS, isDraftValid } from '../hooks/solverReducer'

export function GuessRow({ cells, feedback, isActive, dispatch, onSubmit }) {
  const [focusedCell, setFocusedCell] = useState(0)
  const cellRefs = useRef([])

  function focusCell(index) {
    const clamped = Math.max(0, Math.min(4, index))
    setFocusedCell(clamped)
    cellRefs.current[clamped]?.focus()
  }

  useEffect(() => {
    if (isActive) focusCell(0)
  }, [isActive]) // eslint-disable-line react-hooks/exhaustive-deps

  function handleKeyDown(cellIndex, e) {
    if (!isActive) return

    if (/^[a-zA-Z]$/.test(e.key)) {
      e.preventDefault()
      dispatch({ type: ACTIONS.DISMISS_ERROR })
      dispatch({ type: ACTIONS.SET_GUESS_CHAR, index: cellIndex, char: e.key })
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

      case ' ':
        e.preventDefault()
        dispatch({ type: ACTIONS.CYCLE_FEEDBACK_AT, index: cellIndex })
        break

      case 'Backspace':
        e.preventDefault()
        if (cells[cellIndex] !== '' || feedback[cellIndex] !== 'unset') {
          dispatch({ type: ACTIONS.SET_GUESS_CHAR, index: cellIndex, char: '' })
          dispatch({ type: ACTIONS.SET_FEEDBACK_AT, index: cellIndex, value: 'unset' })
        } else if (cellIndex > 0) {
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
          // Surface validation error in the global error banner
          dispatch({
            type: ACTIONS.SUBMIT_ERROR,
            message: 'Fill all 5 letters and set each tile colour first',
          })
        }
        break

      default:
        break
    }
  }

  const wasAlreadyFocused = useRef(false)

  function handleMouseDown(index) {
    wasAlreadyFocused.current = document.activeElement === cellRefs.current[index]
  }

  function handleTileClick(index) {
    if (!isActive) return
    if (wasAlreadyFocused.current) {
      dispatch({ type: ACTIONS.CYCLE_FEEDBACK_AT, index })
    } else {
      focusCell(index)
    }
  }

  return (
    <div className="flex gap-1.5">
      {cells.map((letter, i) => (
        <GuessTile
          key={i}
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
  )
}
