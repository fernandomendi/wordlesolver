import type { FeedbackValue, HistoryRow, SolverAction, SolverState, Step } from '@/types'

// ── Feedback enum ─────────────────────────────────────────────────────────────
// These are the four possible states for a single tile.
// We use human-readable strings internally; they map to API codes on submit.
export const FEEDBACK = Object.freeze({
  UNSET: 'unset' as const,
  CORRECT: 'correct' as const,
  MISPLACED: 'misplaced' as const,
  ABSENT: 'absent' as const,
})

// Cycle order when the user presses Space or clicks a tile
const FEEDBACK_CYCLE: FeedbackValue[] = [
  FEEDBACK.UNSET,
  FEEDBACK.CORRECT,
  FEEDBACK.MISPLACED,
  FEEDBACK.ABSENT,
]

// Translation table used when building the API payload
const FEEDBACK_TO_CODE: Record<string, string> = {
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
} as const)

// ── Initial state ──────────────────────────────────────────────────────────────
// Exporting INITIAL_STATE lets RESET_ALL return a clean copy without
// duplicating the object literal, and makes testing trivial.
export const INITIAL_STATE: SolverState = {
  language: 'es',
  sessionId: 0,  // increments on reset to re-trigger the opening fetch

  // The row the user is currently typing into — 5 cells + 5 feedback slots.
  draftCells: ['', '', '', '', ''],
  draftFeedback: Array(5).fill(FEEDBACK.UNSET) as FeedbackValue[],

  // Locked rows in submission order: { cells: string[], feedback: FeedbackValue[] }
  history: [],

  isSubmitting: false,
  result: null,   // { best_guess, total_possible, … } from the API
  error: null,    // string | null — surfaces as the dismissible banner
  errorKey: 0,    // increments each error to trigger row shake

  gameOver: false,
  isWin: false,

  // Language-switch confirm flow
  showLanguageResetConfirm: false,
  pendingLanguage: null,
}

// ── Pure helpers ───────────────────────────────────────────────────────────────

/** Convert locked history rows → the `steps` array the API expects. */
export function historyToSteps(history: HistoryRow[]): Step[] {
  return history.map(({ cells, feedback }) => ({
    guess: cells.join('').toLowerCase(),
    answer: feedback.map(f => FEEDBACK_TO_CODE[f]).join(''),
  }))
}

/** True when all 5 cells have a letter and all 5 feedback slots are set. */
export function isDraftValid(cells: string[], feedback: FeedbackValue[]): boolean {
  return (
    cells.every(c => /^[a-zA-Z]$/.test(c)) &&
    feedback.every(f => f !== FEEDBACK.UNSET)
  )
}

/** Advance a feedback value one step around the cycle. */
export function cycleFeedback(current: FeedbackValue): FeedbackValue {
  const idx = FEEDBACK_CYCLE.indexOf(current)
  return FEEDBACK_CYCLE[(idx + 1) % FEEDBACK_CYCLE.length]
}

// ── Reducer ────────────────────────────────────────────────────────────────────
// A reducer is just a function: (currentState, action) → nextState.
// It NEVER mutates state — it always returns a new object.
// The spread operator `{ ...state, field: newValue }` is the main tool.
export function solverReducer(state: SolverState, action: SolverAction): SolverState {
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
      return {
        ...state,
        isSubmitting: false,
        error: action.message || null,
        errorKey: action.message ? state.errorKey + 1 : state.errorKey,
      }

    case ACTIONS.DISMISS_ERROR:
      return { ...state, error: null }

    case ACTIONS.REQUEST_LANGUAGE_CHANGE: {
      // action: { language: 'en' | 'es' }
      // Only count submitted rows as "user progress" — the pre-filled draft
      // suggestion is automatic and shouldn't trigger a confirm dialog.
      const hasData = state.history.length > 0
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
      return { ...INITIAL_STATE, language: state.pendingLanguage!, sessionId: state.sessionId + 1 }

    case ACTIONS.CANCEL_LANGUAGE_CHANGE:
      return { ...state, showLanguageResetConfirm: false, pendingLanguage: null }

    case ACTIONS.RESET_ALL:
      return { ...INITIAL_STATE, language: state.language, sessionId: state.sessionId + 1 }

    default:
      return state
  }
}
