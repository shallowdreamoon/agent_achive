const MetricCard = ({ label, value }) => (
  <div className="rounded border bg-slate-50 p-3">
    <div className="text-xs text-slate-500">{label}</div>
    <div className="text-xl font-semibold">{(value * 100).toFixed(1)}%</div>
  </div>
)

const ScoreBars = ({ perAgent }) => {
  const entries = Object.entries(perAgent || {})
  if (!entries.length) return null
  return (
    <div className="space-y-2">
      {entries.map(([agent, score]) => (
        <div key={agent}>
          <div className="mb-1 flex justify-between text-sm"><span>{agent}</span><span>{(score * 100).toFixed(1)}%</span></div>
          <div className="h-3 rounded bg-slate-200">
            <div className="h-3 rounded bg-indigo-600" style={{ width: `${Math.max(5, score * 100)}%` }} />
          </div>
        </div>
      ))}
    </div>
  )
}

export default function EvalPanel({ benchmark }) {
  if (!benchmark) return null
  const s = benchmark.summary

  return (
    <section className="rounded-2xl bg-white p-4 shadow">
      <h2 className="mb-3 text-lg font-semibold">Benchmark 面板</h2>
      <div className="grid gap-2 md:grid-cols-3">
        <MetricCard label="Overall" value={s.average_overall_score} />
        <MetricCard label="Evidence Hit" value={s.evidence_hit_rate} />
        <MetricCard label="Structured Validity" value={s.structured_output_validity} />
      </div>

      <div className="mt-4">
        <h3 className="mb-2 font-semibold">各 Agent 分数（柱状图）</h3>
        <ScoreBars perAgent={s.per_agent_score} />
      </div>

      <div className="mt-4 overflow-x-auto">
        <h3 className="mb-2 font-semibold">Case 结果</h3>
        <table className="w-full text-sm">
          <thead>
            <tr className="bg-slate-100 text-left">
              <th className="p-2">ID</th><th className="p-2">Agent</th><th className="p-2">Overall</th><th className="p-2">Keyword</th><th className="p-2">Evidence</th>
            </tr>
          </thead>
          <tbody>
            {benchmark.detailed_results.slice(0, 20).map((row) => (
              <tr key={row.id} className="border-b">
                <td className="p-2">{row.id}</td>
                <td className="p-2">{row.agent}</td>
                <td className="p-2">{row.overall_score}</td>
                <td className="p-2">{row.keyword_match}</td>
                <td className="p-2">{row.evidence_hit}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </section>
  )
}
