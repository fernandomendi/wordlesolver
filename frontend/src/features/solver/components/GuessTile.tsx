import { forwardRef } from 'react'
import type { FeedbackValue } from '@/types'

const FEEDBACK_CLASSES: Record<FeedbackValue, string> = {
  unset:     'bg-white text-slate-900 dark:bg-zinc-800 dark:text-zinc-100',
  correct:   'bg-[var(--color-correct)] text-white',
  misplaced: 'bg-[var(--color-misplaced)] text-white',
  absent:    'bg-[var(--color-absent)] text-white',
}

interface GuessTileProps {
  letter: string
  feedback: FeedbackValue
  isActive: boolean
  isFocused: boolean
  onClick: () => void
  onMouseDown: () => void
  onKeyDown: (e: React.KeyboardEvent<HTMLDivElement>) => void
}

// GuessTile renders a single letter cell.
// It's a "dumb" component — it receives everything via props and emits events up.
// No state lives here.
export const GuessTile = forwardRef<HTMLDivElement, GuessTileProps>(
  function GuessTile({ letter, feedback, isActive, isFocused, onClick, onMouseDown, onKeyDown }, ref) {
    const bgClass = FEEDBACK_CLASSES[feedback] ?? FEEDBACK_CLASSES.unset

    const borderClass = isFocused
      ? 'border-[var(--color-tile-border-focus)]'
      : isActive && feedback === 'unset'
        ? 'border-[var(--color-tile-border-active)]'
        : feedback === 'unset'
          ? 'border-[var(--color-tile-border)]'
          : 'border-transparent'

    return (
      <div
        ref={ref}
        role="button"
        // tabIndex 0 = reachable by Tab key. -1 = focusable by code only (inactive rows).
        tabIndex={isActive ? 0 : -1}
        aria-label={`${letter || 'empty'}, ${feedback}`}
        onClick={onClick}
        onMouseDown={onMouseDown}
        onKeyDown={onKeyDown}
        className={[
          'flex h-14 w-14 select-none items-center justify-center',
          'border-2 text-xl font-bold uppercase transition-colors duration-150 outline-none',
          bgClass,
          borderClass,
          isActive ? 'cursor-pointer' : 'cursor-default',
        ].join(' ')}
      >
        {letter}
      </div>
    )
  }
)
