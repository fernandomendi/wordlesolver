import '@testing-library/jest-dom'
import { vi } from 'vitest'

// canvas-confetti uses HTMLCanvasElement which jsdom doesn't support
vi.mock('canvas-confetti', () => ({ default: vi.fn() }))

// useDarkMode calls window.matchMedia which jsdom doesn't implement
Object.defineProperty(window, 'matchMedia', {
  writable: true,
  value: vi.fn().mockImplementation(query => ({
    matches: false,
    media: query,
    addEventListener: vi.fn(),
    removeEventListener: vi.fn(),
  })),
})
