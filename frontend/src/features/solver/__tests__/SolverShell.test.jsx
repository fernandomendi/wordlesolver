import React from 'react'
import { describe, it, expect, vi, beforeEach } from 'vitest'
import { render, screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { SolverShell } from '@/features/solver/components/SolverShell'

// Mock the API client — tests must not make real network calls
vi.mock('@/api/client', () => ({
  solveWordle: vi.fn(),
}))

import { solveWordle } from '@/api/client'

const MOCK_RESULT = { best_guess: 'crane', total_possible: 100 }

beforeEach(() => {
  vi.clearAllMocks()
  // Default: opening fetch succeeds
  solveWordle.mockResolvedValue(MOCK_RESULT)
})

// ── Helper ─────────────────────────────────────────────────────────────────────

function setup() {
  const user = userEvent.setup()
  render(<SolverShell />)
  return { user }
}

// Get the first cell of the active row (always cell 0 of the current draft)
function getActiveCells() {
  return screen.getAllByRole('button').filter(el =>
    el.getAttribute('tabindex') === '0'
  )
}

// ── Typing advances focus ──────────────────────────────────────────────────────

describe('Typing advances cell focus', () => {
  it('typing a letter moves focus to the next cell', async () => {
    const { user } = setup()
    await waitFor(() => expect(solveWordle).toHaveBeenCalledTimes(1))

    const cells = getActiveCells()
    cells[0].focus()
    await user.keyboard('A')
    expect(document.activeElement).toBe(cells[1])
  })

  it('typing on cell 4 stays on cell 4', async () => {
    const { user } = setup()
    await waitFor(() => expect(solveWordle).toHaveBeenCalledTimes(1))

    const cells = getActiveCells()
    cells[4].focus()
    await user.keyboard('Z')
    expect(document.activeElement).toBe(cells[4])
  })
})

// ── Backspace ──────────────────────────────────────────────────────────────────

describe('Backspace behaviour', () => {
  it('clears the current cell if it has a letter', async () => {
    const { user } = setup()
    await waitFor(() => expect(solveWordle).toHaveBeenCalledTimes(1))

    const cells = getActiveCells()
    cells[0].focus()
    await user.keyboard('A')
    cells[0].focus()
    await user.keyboard('[Backspace]')
    expect(cells[0]).toHaveTextContent('')
  })

  it('moves focus left and clears when current cell is already empty', async () => {
    const { user } = setup()
    await waitFor(() => expect(solveWordle).toHaveBeenCalledTimes(1))

    const cells = getActiveCells()
    // Cell 1 is pre-filled with 'r' (from 'crane'). First backspace clears it,
    // leaving cell 1 empty. Second backspace moves left and clears cell 0.
    cells[1].focus()
    await user.keyboard('[Backspace]') // clears 'r', stays on cell 1
    await user.keyboard('[Backspace]') // cell 1 empty → move to cell 0 and clear
    expect(document.activeElement).toBe(cells[0])
    expect(cells[0]).toHaveTextContent('')
  })
})

// ── Space cycles feedback ──────────────────────────────────────────────────────

describe('Space cycles feedback', () => {
  it('cycles unset → correct → misplaced → absent → unset', async () => {
    const { user } = setup()
    await waitFor(() => expect(solveWordle).toHaveBeenCalledTimes(1))

    const cells = getActiveCells()
    cells[0].focus()

    await user.keyboard(' ')
    expect(cells[0]).toHaveAttribute('aria-label', expect.stringContaining('correct'))
    await user.keyboard(' ')
    expect(cells[0]).toHaveAttribute('aria-label', expect.stringContaining('misplaced'))
    await user.keyboard(' ')
    expect(cells[0]).toHaveAttribute('aria-label', expect.stringContaining('absent'))
    await user.keyboard(' ')
    expect(cells[0]).toHaveAttribute('aria-label', expect.stringContaining('unset'))
  })
})

// ── Enter validation ───────────────────────────────────────────────────────────

describe('Enter on invalid row', () => {
  it('shows error banner when row is incomplete', async () => {
    const { user } = setup()
    await waitFor(() => expect(solveWordle).toHaveBeenCalledTimes(1))

    const cells = getActiveCells()
    cells[0].focus()
    // Only type one letter — row is invalid
    await user.keyboard('A[Enter]')
    expect(await screen.findByRole('alert')).toBeInTheDocument()
    expect(solveWordle).toHaveBeenCalledTimes(1) // only opening call, no submit
  })
})

// ── Enter submits valid row ────────────────────────────────────────────────────

describe('Enter on valid row', () => {
  it('submits, locks the row, and advances to the next', async () => {
    solveWordle.mockResolvedValue(MOCK_RESULT)
    const { user } = setup()
    await waitFor(() => expect(solveWordle).toHaveBeenCalledTimes(1))

    const cells = getActiveCells()
    cells[0].focus()

    // Fill all 5 letters
    await user.keyboard('CRANE')
    // Set all 5 feedback to correct via Space
    for (let i = 0; i < 5; i++) {
      getActiveCells()[i].focus()
      await user.keyboard(' ')
    }

    // Submit
    getActiveCells()[0].focus()
    await user.keyboard('[Enter]')

    // API should have been called a second time (the actual submit)
    await waitFor(() => expect(solveWordle).toHaveBeenCalledTimes(2))

    // Previous row is now locked (tabIndex -1)
    const allButtons = screen.getAllByRole('button')
    const lockedCells = allButtons.filter(el => el.getAttribute('tabindex') === '-1')
    expect(lockedCells.length).toBeGreaterThanOrEqual(5)
  })
})

// ── Language confirm-reset ─────────────────────────────────────────────────────

describe('Language change confirm-reset flow', () => {
  it('switches language immediately when grid is empty', async () => {
    const { user } = setup()
    await waitFor(() => expect(solveWordle).toHaveBeenCalledTimes(1))

    const select = screen.getByRole('combobox', { name: /language/i })
    await user.selectOptions(select, 'en')
    // No confirm dialog should appear
    expect(screen.queryByRole('dialog')).not.toBeInTheDocument()
  })

  it('shows confirm dialog when switching with history', async () => {
    solveWordle.mockResolvedValue(MOCK_RESULT)
    const { user } = setup()
    await waitFor(() => expect(solveWordle).toHaveBeenCalledTimes(1))

    // Fill and submit a row
    const cells = getActiveCells()
    cells[0].focus()
    await user.keyboard('CRANE')
    for (let i = 0; i < 5; i++) {
      getActiveCells()[i].focus()
      await user.keyboard(' ')
    }
    getActiveCells()[0].focus()
    await user.keyboard('[Enter]')
    await waitFor(() => expect(solveWordle).toHaveBeenCalledTimes(2))

    // Now switch language
    const select = screen.getByRole('combobox', { name: /language/i })
    await user.selectOptions(select, 'en')
    expect(screen.getByRole('dialog')).toBeInTheDocument()
  })

  it('resets grid on confirm', async () => {
    solveWordle.mockResolvedValue(MOCK_RESULT)
    const { user } = setup()
    await waitFor(() => expect(solveWordle).toHaveBeenCalledTimes(1))

    // Submit a row to populate history
    const cells = getActiveCells()
    cells[0].focus()
    await user.keyboard('CRANE')
    for (let i = 0; i < 5; i++) {
      getActiveCells()[i].focus()
      await user.keyboard(' ')
    }
    getActiveCells()[0].focus()
    await user.keyboard('[Enter]')
    await waitFor(() => expect(solveWordle).toHaveBeenCalledTimes(2))

    // Switch language and confirm
    const select = screen.getByRole('combobox', { name: /language/i })
    await user.selectOptions(select, 'en')
    await user.click(screen.getByText(/reset and switch/i))

    // Grid should be reset — active row cells (tabIndex 0) should be 5 (one row)
    // and no previously locked cells should remain.
    await waitFor(() => {
      const active = screen.getAllByRole('button').filter(el => el.getAttribute('tabindex') === '0')
      expect(active.length).toBe(5)
      // solveWordle called a 3rd time for the new session opening suggestion
      expect(solveWordle).toHaveBeenCalledTimes(3)
    })
  })
})

// ── API error banner ───────────────────────────────────────────────────────────

describe('API error banner', () => {
  it('shows banner with API error message on failed submit', async () => {
    solveWordle
      .mockResolvedValueOnce(MOCK_RESULT) // opening fetch
      .mockRejectedValueOnce(new Error('Contradictory feedback'))
    const { user } = setup()
    await waitFor(() => expect(solveWordle).toHaveBeenCalledTimes(1))

    const cells = getActiveCells()
    cells[0].focus()
    await user.keyboard('CRANE')
    for (let i = 0; i < 5; i++) {
      getActiveCells()[i].focus()
      await user.keyboard(' ')
    }
    getActiveCells()[0].focus()
    await user.keyboard('[Enter]')

    expect(await screen.findByText('Contradictory feedback')).toBeInTheDocument()
  })

  it('dismisses banner on ✕ click', async () => {
    solveWordle
      .mockResolvedValueOnce(MOCK_RESULT)
      .mockRejectedValueOnce(new Error('Contradictory feedback'))
    const { user } = setup()
    await waitFor(() => expect(solveWordle).toHaveBeenCalledTimes(1))

    const cells = getActiveCells()
    cells[0].focus()
    await user.keyboard('CRANE')
    for (let i = 0; i < 5; i++) {
      getActiveCells()[i].focus()
      await user.keyboard(' ')
    }
    getActiveCells()[0].focus()
    await user.keyboard('[Enter]')

    await screen.findByText('Contradictory feedback')
    await user.click(screen.getByLabelText('Dismiss'))
    expect(screen.queryByText('Contradictory feedback')).not.toBeInTheDocument()
  })
})
