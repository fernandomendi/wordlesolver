import type { SolvePayload, SolverResult } from '@/types'

const API_BASE = '/api'

export async function solveWordle(payload: SolvePayload): Promise<SolverResult> {
  const response = await fetch(`${API_BASE}/solve`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(payload),
  })

  if (!response.ok) {
    // Try to surface the API's own error message; fall back to status code.
    let message = `Request failed (${response.status})`
    try {
      const body = await response.json() as { message?: string }
      if (body?.message) message = body.message
    } catch { /* ignore JSON parse failures */ }
    throw new Error(message)
  }

  return response.json() as Promise<SolverResult>
}
