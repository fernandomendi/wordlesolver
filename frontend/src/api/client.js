const API_BASE = '/api'

export async function solveWordle(payload) {
  const response = await fetch(`${API_BASE}/solve`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(payload),
  })

  if (!response.ok) {
    throw new Error(`Solve request failed with status ${response.status}`)
  }

  return response.json()
}
