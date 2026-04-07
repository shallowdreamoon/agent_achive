import { useState } from 'react'
import AgentPanel from './components/AgentPanel'
import EvalPanel from './components/EvalPanel'

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

      <AgentPanel runResult={runResult} />
      <EvalPanel benchmarkResult={benchmarkResult} />
    </div>
  )
}
