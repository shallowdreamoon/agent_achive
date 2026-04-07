import { useState } from 'react'
import AgentPanel from './components/AgentPanel'
import EvalPanel from './components/EvalPanel'

const API_BASE = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000'

export default function App() {
  const [query, setQuery] = useState('我们在美国推出EchoNova音箱，商标风险是什么？')
  const [agentType, setAgentType] = useState('qa')
  const [result, setResult] = useState(null)
  const [benchmark, setBenchmark] = useState(null)
  const [loadingRun, setLoadingRun] = useState(false)
  const [loadingBenchmark, setLoadingBenchmark] = useState(false)
  const [error, setError] = useState('')

  const runAgent = async () => {
    setLoadingRun(true)
    setError('')
    try {
      const resp = await fetch(`${API_BASE}/api/run`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          query,
          agent_type: agentType,
          extra_params: { country: 'US', top_k: 4 },
        }),
      })
      if (!resp.ok) {
        throw new Error(await resp.text())
      }
      const data = await resp.json()
      setResult(data)
    } catch (e) {
      setError(String(e))
    } finally {
      setLoadingRun(false)
    }
  }

  const runBenchmark = async () => {
    setLoadingBenchmark(true)
    setError('')
    try {
      const resp = await fetch(`${API_BASE}/api/benchmark/run`, {
        method: 'POST',
      })
      if (!resp.ok) {
        throw new Error(await resp.text())
      }
      const data = await resp.json()
      setBenchmark(data)
    } catch (e) {
      setError(String(e))
    } finally {
      setLoadingBenchmark(false)
    }
  }

  return (
    <div style={{ padding: '20px', fontFamily: 'Arial, sans-serif' }}>
      <h1>IP Agent Demo</h1>

      <div style={{ marginBottom: '12px' }}>
        <div style={{ marginBottom: '6px' }}>Query</div>
        <textarea
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          rows={5}
          style={{ width: '100%', maxWidth: '900px' }}
        />
      </div>

      <div style={{ marginBottom: '12px' }}>
        <div style={{ marginBottom: '6px' }}>Agent</div>
        <select value={agentType} onChange={(e) => setAgentType(e.target.value)}>
          <option value="qa">qa</option>
          <option value="layout">layout</option>
          <option value="litigation">litigation</option>
        </select>
      </div>

      <div style={{ display: 'flex', gap: '8px', marginBottom: '12px' }}>
        <button onClick={runAgent} disabled={loadingRun}>
          {loadingRun ? 'Running...' : 'POST /api/run'}
        </button>
        <button onClick={runBenchmark} disabled={loadingBenchmark}>
          {loadingBenchmark ? 'Running...' : 'POST /api/benchmark/run'}
        </button>
      </div>

      {error && <div style={{ color: 'red', marginBottom: '12px' }}>{error}</div>}

      <AgentPanel result={result} />
      <EvalPanel benchmark={benchmark} />
    </div>
  )
}
