import confetti from 'canvas-confetti'

export function useConfetti(): { fire: () => void } {
  function fire() {
    const shared = {
      particleCount: 80,
      spread: 70,
      startVelocity: 55,
      ticks: 200,
      colors: ['#6aaa64', '#c9b458', '#ffffff', '#3b82f6'],
    }
    confetti({ ...shared, origin: { x: 0.1, y: 1 }, angle: 60 })
    confetti({ ...shared, origin: { x: 0.9, y: 1 }, angle: 120 })
  }

  return { fire }
}
