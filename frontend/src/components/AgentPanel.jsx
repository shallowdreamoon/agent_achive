export default function AgentPanel({ result }) {
  if (!result) return null
  return (
    <div className="rounded-xl bg-white p-4 shadow">
      <h3 className="mb-2 text-lg font-semibold">结构化输出</h3>
      <pre className="rounded bg-slate-100 p-3 text-sm overflow-x-auto">{JSON.stringify(result.answer, null, 2)}</pre>
      <h3 className="mb-2 mt-4 text-lg font-semibold">证据来源</h3>
      <div className="space-y-2">
        {result.evidence.map((ev) => (
          <div key={ev.id} className="rounded border border-slate-200 p-2">
            <div className="font-medium">{ev.id} | {ev.title}</div>
            <div className="text-sm text-slate-600">{ev.content}</div>
            <div className="text-xs text-slate-500">score={ev.score} country={ev.country} task={ev.task}</div>
          </div>
        ))}
      </div>
    </div>
  )
}
