import { useMemo } from 'react'

export function useSolver() {
  return useMemo(
    () => ({
      status: 'idle',
    }),
    [],
  )
}
