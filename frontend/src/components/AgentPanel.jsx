export default function AgentPanel({ result }) {
  if (!result) return null

  const copyJson = async () => {
    await navigator.clipboard.writeText(JSON.stringify(result.structured_result, null, 2))
  }

  return (
    <section className="rounded-2xl bg-white p-4 shadow">
      <div className="mb-3 flex items-center justify-between">
        <h2 className="text-lg font-semibold">Agent 输出</h2>
        <button onClick={copyJson} className="rounded border px-2 py-1 text-sm">复制 JSON</button>
      </div>

      <div className="mb-3 rounded bg-slate-50 p-3 text-sm">
        <p><b>selected_agent:</b> {result.selected_agent}</p>
        <p><b>routing_reason:</b> {result.routing_reason}</p>
        <p><b>latency_ms:</b> {result.latency_ms}</p>
      </div>

      <h3 className="mb-2 font-semibold">结构化结果</h3>
      <pre className="overflow-x-auto rounded bg-slate-100 p-3 text-xs">{JSON.stringify(result.structured_result, null, 2)}</pre>

      <h3 className="mb-2 mt-4 font-semibold">证据</h3>
      <div className="space-y-2">
        {result.evidence.map((ev) => (
          <details key={ev.id} className="rounded border border-slate-200 p-2">
            <summary className="cursor-pointer text-sm font-medium">{ev.id} | {ev.title} (score={ev.score})</summary>
            <p className="mt-2 text-sm text-slate-700">{ev.snippet}</p>
            <p className="mt-1 text-xs text-slate-500">task={ev.task} country={ev.country}</p>
          </details>
        ))}
      </div>
    </section>
  )
}
