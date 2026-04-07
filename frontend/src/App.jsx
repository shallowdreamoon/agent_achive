import { useState } from 'react'
import AgentPanel from './components/AgentPanel'
import EvalPanel from './components/EvalPanel'

const API = import.meta.env.VITE_API_URL || 'http://localhost:8000'

export default function App() {
  const [agent, setAgent] = useState('qa')
  const [query, setQuery] = useState('我们在美国销售智能音箱，商标是否会侵权？')
  const [country, setCountry] = useState('US')
  const [result, setResult] = useState(null)
  const [evalResult, setEvalResult] = useState(null)

  const runAgent = async () => {
    const res = await fetch(`${API}/api/agent`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ agent, query, country })
    })
    setResult(await res.json())
  }

  const runEval = async () => {
    const res = await fetch(`${API}/api/evaluate`)
    setEvalResult(await res.json())
  }

  return (
    <main className="mx-auto max-w-6xl p-6">
      <h1 className="mb-4 text-2xl font-bold">IPBench Overseas IP Risk Agent System</h1>
      <div className="grid gap-4 md:grid-cols-3">
        <div className="rounded-xl bg-white p-4 shadow md:col-span-1">
          <label className="mb-1 block text-sm">Agent</label>
          <select value={agent} onChange={(e) => setAgent(e.target.value)} className="mb-3 w-full rounded border p-2">
            <option value="qa">IP Risk QA Agent</option>
            <option value="layout">IP Layout Planning Agent</option>
            <option value="litigation">IP Litigation Analysis Agent</option>
          </select>
          <label className="mb-1 block text-sm">Country</label>
          <input value={country} onChange={(e) => setCountry(e.target.value)} className="mb-3 w-full rounded border p-2" />
          <label className="mb-1 block text-sm">Input</label>
          <textarea value={query} onChange={(e) => setQuery(e.target.value)} className="mb-3 h-32 w-full rounded border p-2" />
          <div className="flex gap-2">
            <button onClick={runAgent} className="rounded bg-indigo-600 px-3 py-2 text-white">运行 Agent</button>
            <button onClick={runEval} className="rounded bg-emerald-600 px-3 py-2 text-white">运行评估</button>
          </div>
        </div>
        <div className="md:col-span-2 space-y-4">
          <AgentPanel result={result} />
          <EvalPanel evalResult={evalResult} />
        </div>
      </div>
    </main>
  )
}
