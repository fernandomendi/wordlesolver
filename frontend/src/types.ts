// ── Language ───────────────────────────────────────────────────────────────────
export type Language = 'en' | 'es'

// ── Theme ──────────────────────────────────────────────────────────────────────
export type ThemePreference = 'light' | 'dark' | 'system'

// ── API shapes ─────────────────────────────────────────────────────────────────
export interface WordEntry {
  word: string
}

export interface SolverResult {
  best_guess: string | null
  total_possible: number
  possible_words: WordEntry[]
  suggestions: WordEntry[]
}

export interface Step {
  guess: string   // 5-letter lowercase word
  answer: string  // 5-char code, each digit 0 (correct) | 1 (misplaced) | 2 (absent)
}

export interface SolvePayload {
  language: Language
  steps: Step[]
}

// ── Solver state ───────────────────────────────────────────────────────────────
export type FeedbackValue = 'unset' | 'correct' | 'misplaced' | 'absent'

export interface HistoryRow {
  cells: string[]
  feedback: FeedbackValue[]
}

export interface SolverState {
  // app-wide — candidate for AppContext when a second feature needs it
  // language is now owned by AppContext; SolverState holds only solver concerns
  sessionId: number
  draftCells: string[]
  draftFeedback: FeedbackValue[]
  history: HistoryRow[]
  isSubmitting: boolean
  result: SolverResult | null
  error: string | null
  errorKey: number
  gameOver: boolean
  isWin: boolean
  showLanguageResetConfirm: boolean
  pendingLanguage: Language | null
}

// ── Reducer action union ───────────────────────────────────────────────────────
// Discriminated union: each action has a unique `type` literal.
// TypeScript narrows the type inside each `case` branch automatically.
export type SolverAction =
  | { type: 'SET_GUESS_CHAR';        index: number; char: string }
  | { type: 'CYCLE_FEEDBACK_AT';     index: number }
  | { type: 'SET_FEEDBACK_AT';       index: number; value: FeedbackValue }
  | { type: 'ADD_STEP_FROM_DRAFT' }
  | { type: 'SUBMIT_START' }
  | { type: 'SUBMIT_SUCCESS';        result: SolverResult; isWin: boolean }
  | { type: 'SUBMIT_ERROR';          message: string | null }
  | { type: 'DISMISS_ERROR' }
  | { type: 'SHOW_LANGUAGE_CONFIRM';   language: Language }
  | { type: 'HIDE_LANGUAGE_CONFIRM' }
  | { type: 'RESET_ALL' }
