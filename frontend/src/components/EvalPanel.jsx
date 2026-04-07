const MetricBar = ({ name, value }) => (
  <div>
    <div className="mb-1 flex justify-between text-sm"><span>{name}</span><span>{(value * 100).toFixed(1)}%</span></div>
    <div className="h-2 rounded bg-slate-200"><div className="h-2 rounded bg-indigo-600" style={{ width: `${Math.min(100, value * 100)}%` }} /></div>
  </div>
)

export default function EvalPanel({ evalResult }) {
  if (!evalResult) return null
  return (
    <div className="rounded-xl bg-white p-4 shadow">
      <h3 className="mb-3 text-lg font-semibold">Benchmark 指标</h3>
      <div className="space-y-3">
        <MetricBar name="Accuracy" value={evalResult.accuracy} />
        <MetricBar name="Reasoning Score" value={evalResult.reasoning_score} />
        <MetricBar name="Task Coverage" value={evalResult.task_coverage} />
      </div>
    </div>
  )
}
