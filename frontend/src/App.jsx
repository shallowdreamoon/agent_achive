import { useState } from 'react'

const API_BASE = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000'

export default function App() {
  const [agentType, setAgentType] = useState('qa')
  const [query, setQuery] = useState('我们在美国推出EchoNova音箱，商标风险是什么？')
  const [runResult, setRunResult] = useState(null)
  const [benchmarkResult, setBenchmarkResult] = useState(null)
  const [error, setError] = useState('')

  const handleRun = async () => {
    setError('')
    try {
      const resp = await fetch(`${API_BASE}/api/run`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query, agent_type: agentType }),
      })
      if (!resp.ok) throw new Error(await resp.text())
      setRunResult(await resp.json())
    } catch (e) {
      setError(String(e))
    }
  }

  const handleBenchmark = async () => {
    setError('')
    try {
      const resp = await fetch(`${API_BASE}/api/benchmark/run`, { method: 'POST' })
      if (!resp.ok) throw new Error(await resp.text())
      setBenchmarkResult(await resp.json())
    } catch (e) {
      setError(String(e))
    }
  }

  return (
    <div style={{ padding: 20, fontFamily: 'Arial, sans-serif', maxWidth: 960 }}>
      <h1>Multi-Agent Mock Demo</h1>

      <div style={{ marginBottom: 12 }}>
        <div>Agent</div>
        <select value={agentType} onChange={(e) => setAgentType(e.target.value)}>
          <option value="qa">qa</option>
          <option value="layout">layout</option>
          <option value="litigation">litigation</option>
        </select>
      </div>

      <div style={{ marginBottom: 12 }}>
        <div>Query</div>
        <textarea rows={4} style={{ width: '100%' }} value={query} onChange={(e) => setQuery(e.target.value)} />
      </div>

      <div style={{ marginBottom: 12 }}>
        <button onClick={handleRun}>Run</button>
        <button onClick={handleBenchmark} style={{ marginLeft: 8 }}>Benchmark</button>
      </div>

      {error && <div style={{ color: 'red', marginBottom: 12 }}>{error}</div>}

      {runResult && (
        <div style={{ border: '1px solid #ccc', padding: 12, marginBottom: 12 }}>
          <div><b>selected_agent:</b> {runResult.selected_agent}</div>
          <div><b>routing_reason:</b> {runResult.routing_reason}</div>
          <div><b>structured_result:</b></div>
          <pre>{JSON.stringify(runResult.structured_result, null, 2)}</pre>
          <div><b>evidence:</b></div>
          <ul>
            {(runResult.evidence || []).map((item) => (
              <li key={item.id}>{item.id} - {item.title}</li>
            ))}
          </ul>
        </div>
      )}

      {benchmarkResult && (
        <div style={{ border: '1px solid #ccc', padding: 12 }}>
          <div><b>benchmark summary:</b></div>
          <pre>{JSON.stringify(benchmarkResult.summary, null, 2)}</pre>
        </div>
      )}
    </div>
  )
}
