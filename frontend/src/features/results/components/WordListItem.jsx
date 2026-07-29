// Single word entry faded by its rank (0 = full opacity, 9 = ~25% opacity).
export function WordListItem({ word, rank }) {
  const opacity = 1 - (rank / 9) * 0.75
  return (
    <li
      className="py-0.5 font-mono text-sm uppercase tracking-widest text-slate-700"
      style={{ opacity }}
    >
      {word}
    </li>
  )
}
