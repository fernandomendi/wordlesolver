import { useSolver } from '../hooks/useSolver'

export function SolverShell() {
  const { status } = useSolver()

  return (
    <main className="mx-auto flex min-h-screen w-full max-w-4xl items-center justify-center px-6 py-16">
      <section className="w-full rounded-2xl border border-slate-200 bg-white p-8 shadow-sm">
        <p className="text-sm font-medium uppercase tracking-wide text-emerald-700">Wordle Solver</p>
        <h1 className="mt-2 text-3xl font-semibold tracking-tight text-slate-900">React frontend scaffold ready</h1>
        <p className="mt-3 text-slate-600">
          Next steps: guess input, feedback grid, and API solve flow.
        </p>

        <div className="mt-6 rounded-lg bg-slate-50 px-4 py-3 text-sm text-slate-700">
          Solver hook status: <span className="font-semibold">{status}</span>
        </div>
      </section>
    </main>
  )
}
