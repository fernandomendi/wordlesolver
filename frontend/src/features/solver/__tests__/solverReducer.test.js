import { describe, it, expect } from 'vitest'
import {
  solverReducer,
  INITIAL_STATE,
  ACTIONS,
  FEEDBACK,
  cycleFeedback,
  isDraftValid,
  historyToSteps,
} from '../hooks/solverReducer'

// ── cycleFeedback ──────────────────────────────────────────────────────────────

describe('cycleFeedback', () => {
  it('cycles unset → correct → misplaced → absent → unset', () => {
    expect(cycleFeedback(FEEDBACK.UNSET)).toBe(FEEDBACK.CORRECT)
    expect(cycleFeedback(FEEDBACK.CORRECT)).toBe(FEEDBACK.MISPLACED)
    expect(cycleFeedback(FEEDBACK.MISPLACED)).toBe(FEEDBACK.ABSENT)
    expect(cycleFeedback(FEEDBACK.ABSENT)).toBe(FEEDBACK.UNSET)
  })
})

// ── isDraftValid ───────────────────────────────────────────────────────────────

describe('isDraftValid', () => {
  it('returns true when all 5 cells have a letter and all feedback is set', () => {
    const cells = ['w', 'o', 'r', 'l', 'd']
    const feedback = Array(5).fill(FEEDBACK.CORRECT)
    expect(isDraftValid(cells, feedback)).toBe(true)
  })

  it('returns false when any cell is empty', () => {
    const cells = ['w', 'o', '', 'l', 'd']
    const feedback = Array(5).fill(FEEDBACK.CORRECT)
    expect(isDraftValid(cells, feedback)).toBe(false)
  })

  it('returns false when any feedback is unset', () => {
    const cells = ['w', 'o', 'r', 'l', 'd']
    const feedback = [FEEDBACK.CORRECT, FEEDBACK.CORRECT, FEEDBACK.UNSET, FEEDBACK.CORRECT, FEEDBACK.CORRECT]
    expect(isDraftValid(cells, feedback)).toBe(false)
  })

  it('returns false when both cells and feedback are incomplete', () => {
    expect(isDraftValid(['', '', '', '', ''], Array(5).fill(FEEDBACK.UNSET))).toBe(false)
  })
})

// ── historyToSteps ─────────────────────────────────────────────────────────────

describe('historyToSteps', () => {
  it('converts history rows to API step format', () => {
    const history = [
      { cells: ['W', 'O', 'R', 'L', 'D'], feedback: [FEEDBACK.CORRECT, FEEDBACK.ABSENT, FEEDBACK.MISPLACED, FEEDBACK.ABSENT, FEEDBACK.CORRECT] },
    ]
    expect(historyToSteps(history)).toEqual([
      { guess: 'world', answer: '02120' },
    ])
  })

  it('returns empty array for empty history', () => {
    expect(historyToSteps([])).toEqual([])
  })
})

// ── reducer ────────────────────────────────────────────────────────────────────

describe('solverReducer', () => {
  it('SET_GUESS_CHAR updates the correct cell', () => {
    const state = solverReducer(INITIAL_STATE, { type: ACTIONS.SET_GUESS_CHAR, index: 2, char: 'A' })
    expect(state.draftCells[2]).toBe('A')
    expect(state.draftCells[0]).toBe('')  // others untouched
  })

  it('CYCLE_FEEDBACK_AT advances the feedback cycle', () => {
    const state = solverReducer(INITIAL_STATE, { type: ACTIONS.CYCLE_FEEDBACK_AT, index: 0 })
    expect(state.draftFeedback[0]).toBe(FEEDBACK.CORRECT)
  })

  it('SET_FEEDBACK_AT sets a specific feedback value', () => {
    const state = solverReducer(INITIAL_STATE, { type: ACTIONS.SET_FEEDBACK_AT, index: 3, value: FEEDBACK.ABSENT })
    expect(state.draftFeedback[3]).toBe(FEEDBACK.ABSENT)
  })

  it('ADD_STEP_FROM_DRAFT moves draft into history and resets draft', () => {
    let state = { ...INITIAL_STATE, draftCells: ['w', 'o', 'r', 'l', 'd'], draftFeedback: Array(5).fill(FEEDBACK.CORRECT) }
    state = solverReducer(state, { type: ACTIONS.ADD_STEP_FROM_DRAFT })
    expect(state.history).toHaveLength(1)
    expect(state.history[0].cells).toEqual(['w', 'o', 'r', 'l', 'd'])
    expect(state.draftCells).toEqual(['', '', '', '', ''])
    expect(state.draftFeedback).toEqual(Array(5).fill(FEEDBACK.UNSET))
  })

  it('SUBMIT_START sets isSubmitting and clears error', () => {
    const state = solverReducer({ ...INITIAL_STATE, error: 'oops' }, { type: ACTIONS.SUBMIT_START })
    expect(state.isSubmitting).toBe(true)
    expect(state.error).toBeNull()
  })

  it('SUBMIT_SUCCESS stores result and sets gameOver on win', () => {
    const result = { best_guess: 'crane', total_possible: 1 }
    const state = solverReducer(INITIAL_STATE, { type: ACTIONS.SUBMIT_SUCCESS, result, isWin: true })
    expect(state.result).toBe(result)
    expect(state.gameOver).toBe(true)
    expect(state.isWin).toBe(true)
    expect(state.isSubmitting).toBe(false)
  })

  it('SUBMIT_SUCCESS does not set gameOver when not a win and under 6 rows', () => {
    const result = { best_guess: 'crane', total_possible: 10 }
    const state = solverReducer(INITIAL_STATE, { type: ACTIONS.SUBMIT_SUCCESS, result, isWin: false })
    expect(state.gameOver).toBe(false)
  })

  it('SUBMIT_ERROR stores error message', () => {
    const state = solverReducer(INITIAL_STATE, { type: ACTIONS.SUBMIT_ERROR, message: 'bad input' })
    expect(state.error).toBe('bad input')
    expect(state.isSubmitting).toBe(false)
  })

  it('DISMISS_ERROR clears error', () => {
    const state = solverReducer({ ...INITIAL_STATE, error: 'oops' }, { type: ACTIONS.DISMISS_ERROR })
    expect(state.error).toBeNull()
  })

  it('RESET_ALL resets to initial state but keeps language', () => {
    const dirty = { ...INITIAL_STATE, language: 'es', history: [{ cells: ['a', 'b', 'c', 'd', 'e'], feedback: [] }], error: 'oops' }
    const state = solverReducer(dirty, { type: ACTIONS.RESET_ALL })
    expect(state.language).toBe('es')
    expect(state.history).toHaveLength(0)
    expect(state.error).toBeNull()
    expect(state.sessionId).toBe(1)
  })

  it('REQUEST_LANGUAGE_CHANGE switches immediately when no data', () => {
    const state = solverReducer(INITIAL_STATE, { type: ACTIONS.REQUEST_LANGUAGE_CHANGE, language: 'es' })
    expect(state.language).toBe('es')
    expect(state.showLanguageResetConfirm).toBe(false)
  })

  it('REQUEST_LANGUAGE_CHANGE shows confirm when history exists', () => {
    const withHistory = { ...INITIAL_STATE, history: [{ cells: ['a','b','c','d','e'], feedback: [] }] }
    const state = solverReducer(withHistory, { type: ACTIONS.REQUEST_LANGUAGE_CHANGE, language: 'es' })
    expect(state.showLanguageResetConfirm).toBe(true)
    expect(state.pendingLanguage).toBe('es')
  })

  it('CONFIRM_LANGUAGE_CHANGE resets all and switches language', () => {
    const s = { ...INITIAL_STATE, pendingLanguage: 'es', showLanguageResetConfirm: true, history: [{}] }
    const state = solverReducer(s, { type: ACTIONS.CONFIRM_LANGUAGE_CHANGE })
    expect(state.language).toBe('es')
    expect(state.history).toHaveLength(0)
    expect(state.showLanguageResetConfirm).toBe(false)
  })

  it('CANCEL_LANGUAGE_CHANGE closes confirm without switching', () => {
    const s = { ...INITIAL_STATE, pendingLanguage: 'es', showLanguageResetConfirm: true }
    const state = solverReducer(s, { type: ACTIONS.CANCEL_LANGUAGE_CHANGE })
    expect(state.showLanguageResetConfirm).toBe(false)
    expect(state.pendingLanguage).toBeNull()
    expect(state.language).toBe(INITIAL_STATE.language)
  })
})
