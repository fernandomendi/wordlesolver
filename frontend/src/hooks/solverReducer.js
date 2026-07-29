// ── Feedback enum ─────────────────────────────────────────────────────────────
// These are the four possible states for a single tile.
// We use human-readable strings internally; they map to API codes on submit.
export const FEEDBACK = Object.freeze({
  UNSET: 'unset',       // white — user hasn't set this tile yet
  CORRECT: 'correct',   // green — right letter, right position  → API "0"
  MISPLACED: 'misplaced', // yellow — right letter, wrong position → API "1"
  ABSENT: 'absent',     // grey — letter not in word at all       → API "2"
})

// Cycle order when the user presses Space or clicks a tile
const FEEDBACK_CYCLE = [
  FEEDBACK.UNSET,
  FEEDBACK.CORRECT,
  FEEDBACK.MISPLACED,
  FEEDBACK.ABSENT,
]

// Translation table used when building the API payload
const FEEDBACK_TO_CODE = {
  [FEEDBACK.CORRECT]: '0',
  [FEEDBACK.MISPLACED]: '1',
  [FEEDBACK.ABSENT]: '2',
}

// ── Action type constants ──────────────────────────────────────────────────────
// Plain string constants so the reducer switch and every dispatch() call
// share the same spelling — a typo becomes a no-op you can catch at runtime.
export const ACTIONS = Object.freeze({
  SET_GUESS_CHAR: 'SET_GUESS_CHAR',       // user typed a letter in one cell
  CYCLE_FEEDBACK_AT: 'CYCLE_FEEDBACK_AT', // Space/click cycled a tile status
  SET_FEEDBACK_AT: 'SET_FEEDBACK_AT',     // programmatic tile status set
  ADD_STEP_FROM_DRAFT: 'ADD_STEP_FROM_DRAFT', // Enter pressed on valid row
  SUBMIT_START: 'SUBMIT_START',
  SUBMIT_SUCCESS: 'SUBMIT_SUCCESS',
  SUBMIT_ERROR: 'SUBMIT_ERROR',
  DISMISS_ERROR: 'DISMISS_ERROR',
  REQUEST_LANGUAGE_CHANGE: 'REQUEST_LANGUAGE_CHANGE',
  CONFIRM_LANGUAGE_CHANGE: 'CONFIRM_LANGUAGE_CHANGE',
  CANCEL_LANGUAGE_CHANGE: 'CANCEL_LANGUAGE_CHANGE',
  RESET_ALL: 'RESET_ALL',
})

// ── Initial state ──────────────────────────────────────────────────────────────
// Exporting INITIAL_STATE lets RESET_ALL return a clean copy without
// duplicating the object literal, and makes testing trivial.
export const INITIAL_STATE = {
  language: 'es',
  sessionId: 0,  // increments on reset to re-trigger the opening fetch

  // The row the user is currently typing into — 5 cells + 5 feedback slots.
  draftCells: ['', '', '', '', ''],
  draftFeedback: Array(5).fill(FEEDBACK.UNSET),

  // Locked rows in submission order: { cells: string[], feedback: string[] }
  history: [],

  isSubmitting: false,
  result: null,   // { best_guess, total_possible, … } from the API
  error: null,    // string | null — surfaces as the dismissible banner

  gameOver: false,
  isWin: false,

  // Language-switch confirm flow
  showLanguageResetConfirm: false,
  pendingLanguage: null,
}

// ── Pure helpers ───────────────────────────────────────────────────────────────

/** Convert locked history rows → the `steps` array the API expects. */
export function historyToSteps(history) {
  return history.map(({ cells, feedback }) => ({
    guess: cells.join('').toLowerCase(),
    answer: feedback.map(f => FEEDBACK_TO_CODE[f]).join(''),
  }))
}

/** True when all 5 cells have a letter and all 5 feedback slots are set. */
export function isDraftValid(cells, feedback) {
  return (
    cells.every(c => /^[a-zA-Z]$/.test(c)) &&
    feedback.every(f => f !== FEEDBACK.UNSET)
  )
}

/** Advance a feedback value one step around the cycle. */
export function cycleFeedback(current) {
  const idx = FEEDBACK_CYCLE.indexOf(current)
  return FEEDBACK_CYCLE[(idx + 1) % FEEDBACK_CYCLE.length]
}

// ── Reducer ────────────────────────────────────────────────────────────────────
// A reducer is just a function: (currentState, action) → nextState.
// It NEVER mutates state — it always returns a new object.
// The spread operator `{ ...state, field: newValue }` is the main tool.
export function solverReducer(state, action) {
  switch (action.type) {

    case ACTIONS.SET_GUESS_CHAR: {
      // action: { index: 0-4, char: string }
      const next = [...state.draftCells]
      next[action.index] = action.char
      return { ...state, draftCells: next }
    }

    case ACTIONS.CYCLE_FEEDBACK_AT: {
      // action: { index: 0-4 }
      const next = [...state.draftFeedback]
      next[action.index] = cycleFeedback(next[action.index])
      return { ...state, draftFeedback: next }
    }

    case ACTIONS.SET_FEEDBACK_AT: {
      // action: { index: 0-4, value: FEEDBACK.* }
      const next = [...state.draftFeedback]
      next[action.index] = action.value
      return { ...state, draftFeedback: next }
    }

    case ACTIONS.ADD_STEP_FROM_DRAFT: {
      // Lock the current draft row into history and reset the draft.
      const newHistory = [
        ...state.history,
        { cells: [...state.draftCells], feedback: [...state.draftFeedback] },
      ]
      return {
        ...state,
        history: newHistory,
        draftCells: ['', '', '', '', ''],
        draftFeedback: Array(5).fill(FEEDBACK.UNSET),
      }
    }

    case ACTIONS.SUBMIT_START:
      return { ...state, isSubmitting: true, error: null }

    case ACTIONS.SUBMIT_SUCCESS:
      return {
        ...state,
        isSubmitting: false,
        result: action.result,
        gameOver: action.isWin || state.history.length >= 6,
        isWin: action.isWin,
      }

    case ACTIONS.SUBMIT_ERROR:
      return { ...state, isSubmitting: false, error: action.message || null }

    case ACTIONS.DISMISS_ERROR:
      return { ...state, error: null }

    case ACTIONS.REQUEST_LANGUAGE_CHANGE: {
      // action: { language: 'en' | 'es' }
      const hasData =
        state.history.length > 0 || state.draftCells.some(c => c !== '')
      if (hasData) {
        // User has unsaved progress → show the confirm dialog
        return {
          ...state,
          showLanguageResetConfirm: true,
          pendingLanguage: action.language,
        }
      }
      // No progress → switch immediately
      return { ...state, language: action.language }
    }

    case ACTIONS.CONFIRM_LANGUAGE_CHANGE:
      return { ...INITIAL_STATE, language: state.pendingLanguage, sessionId: state.sessionId + 1 }

    case ACTIONS.CANCEL_LANGUAGE_CHANGE:
      return { ...state, showLanguageResetConfirm: false, pendingLanguage: null }

    case ACTIONS.RESET_ALL:
      return { ...INITIAL_STATE, language: state.language, sessionId: state.sessionId + 1 }

    default:
      return state
  }
}
