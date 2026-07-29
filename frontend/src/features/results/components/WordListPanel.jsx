import { WordListItem } from './WordListItem'

function WordList({ title, items, keyProp }) {
  return (
    <div className="flex flex-col gap-2">
      <h3 className="text-xs font-semibold uppercase tracking-widest text-slate-400 dark:text-slate-500">
        {title}
      </h3>
      {items.length === 0 ? (
        <p className="text-xs text-slate-300 dark:text-slate-600">—</p>
      ) : (
        <ol className="list-none space-y-0.5">
          {items.map((item, i) => (
            <WordListItem key={item[keyProp]} word={item[keyProp]} rank={i} />
          ))}
        </ol>
      )}
    </div>
  )
}

// Displays top-10 possible words and top-10 suggestions side by side.
// Both lists fade from full opacity (rank 0) to ~25% (rank 9).
export function WordListPanel({ result, isLoading }) {
  const possibleWords = result?.possible_words ?? []
  const suggestions = result?.suggestions ?? []
  const total = result?.total_possible ?? null

  if (isLoading) {
    return (
      <div className="flex flex-col gap-4">
        <div className="h-4 w-32 animate-pulse rounded bg-slate-200 dark:bg-slate-600" />
        <div className="flex gap-8">
          {[0, 1].map(col => (
            <div key={col} className="flex flex-col gap-2">
              <div className="h-3 w-20 animate-pulse rounded bg-slate-200 dark:bg-slate-600" />
              {Array.from({ length: 10 }, (_, i) => (
                <div
                  key={i}
                  className="h-4 animate-pulse rounded bg-slate-100 dark:bg-slate-700"
                  style={{ width: `${70 - i * 4}%`, opacity: 1 - (i / 9) * 0.75 }}
                />
              ))}
            </div>
          ))}
        </div>
      </div>
    )
  }

  return (
    <div className="flex flex-col gap-4">
      <p className="text-sm text-slate-500 dark:text-slate-400">
        <span className="font-semibold text-slate-900 dark:text-slate-100">{total ?? '—'}</span>
        {' '}possible {total === 1 ? 'word' : 'words'} remaining
      </p>
      <div className="flex gap-8">
        <WordList title="Possible words" items={possibleWords} keyProp="word" />
        <WordList title="Suggestions" items={suggestions} keyProp="word" />
      </div>
    </div>
  )
}
