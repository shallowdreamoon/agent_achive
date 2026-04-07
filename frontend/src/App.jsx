import { useMemo, useState } from 'react'
import AgentPanel from './components/AgentPanel'
import EvalPanel from './components/EvalPanel'

const API = import.meta.env.VITE_API_URL || 'http://localhost:8000'

const examples = {
  qa: '我们在美国销售智能音箱，商标是否会侵权？',
  layout: '电池管理算法进入美国和加拿大，如何做专利布局？',
  litigation: '收到美国NPE专利警告函，应诉路径是什么？',
}

export default function App() {
  const [agentType, setAgentType] = useState('auto')
  const [query, setQuery] = useState(examples.qa)
  const [country, setCountry] = useState('US')
  const [topK, setTopK] = useState(4)
  const [result, setResult] = useState(null)
  const [benchmark, setBenchmark] = useState(null)
  const [loadingRun, setLoadingRun] = useState(false)
  const [loadingBench, setLoadingBench] = useState(false)
  const [error, setError] = useState('')

  const runAgent = async () => {
    setLoadingRun(true)
    setError('')
    try {
      const payload = {
        query,
        agent_type: agentType === 'auto' ? null : agentType,
        extra_params: { country, top_k: Number(topK) },
      }
      const res = await fetch(`${API}/api/run`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      })
      if (!res.ok) throw new Error(await res.text())
      setResult(await res.json())
    } catch (e) {
      setError(String(e))
    } finally {
      setLoadingRun(false)
    }
  }

  const runBenchmark = async () => {
    setLoadingBench(true)
    setError('')
    try {
      const res = await fetch(`${API}/api/benchmark/run`, { method: 'POST' })
      if (!res.ok) throw new Error(await res.text())
      setBenchmark(await res.json())
    } catch (e) {
      setError(String(e))
    } finally {
      setLoadingBench(false)
    }
  }

  const selectedExample = useMemo(() => {
    if (agentType === 'auto') return examples.qa
    return examples[agentType]
  }, [agentType])

  return (
    <main className="min-h-screen bg-slate-100 p-6 text-slate-900">
      <div className="mx-auto max-w-7xl space-y-4">
        <header className="rounded-2xl bg-white p-6 shadow">
          <h1 className="text-2xl font-bold">企业出海知识产权风险多智能体系统</h1>
          <p className="mt-2 text-sm text-slate-600">支持三类 agent、自动路由、证据检索、结构化推理和 benchmark 评估。</p>
        </header>

        {error && <div className="rounded-xl border border-red-200 bg-red-50 p-3 text-red-700">{error}</div>}

        <div className="grid gap-4 lg:grid-cols-3">
          <section className="rounded-2xl bg-white p-4 shadow lg:col-span-1">
            <label className="mb-1 block text-sm font-semibold">Agent 模式</label>
            <select className="mb-3 w-full rounded border p-2" value={agentType} onChange={(e) => setAgentType(e.target.value)}>
              <option value="auto">自动路由</option>
              <option value="qa">IP Risk QA Agent</option>
              <option value="layout">IP Layout Planning Agent</option>
              <option value="litigation">IP Litigation Analysis Agent</option>
            </select>
            <label className="mb-1 block text-sm font-semibold">输入问题</label>
            <textarea className="mb-3 h-36 w-full rounded border p-2" value={query} onChange={(e) => setQuery(e.target.value)} />
            <button className="mb-3 text-xs text-indigo-600 underline" onClick={() => setQuery(selectedExample)}>填充示例</button>
            <label className="mb-1 block text-sm font-semibold">目标国家/地区</label>
            <input className="mb-3 w-full rounded border p-2" value={country} onChange={(e) => setCountry(e.target.value)} />
            <label className="mb-1 block text-sm font-semibold">Top-K 证据</label>
            <input className="mb-3 w-full rounded border p-2" type="number" min="1" max="8" value={topK} onChange={(e) => setTopK(e.target.value)} />
            <div className="flex gap-2">
              <button onClick={runAgent} disabled={loadingRun} className="rounded bg-indigo-600 px-3 py-2 text-white disabled:opacity-40">{loadingRun ? '运行中...' : '运行 Agent'}</button>
              <button onClick={runBenchmark} disabled={loadingBench} className="rounded bg-emerald-600 px-3 py-2 text-white disabled:opacity-40">{loadingBench ? '评估中...' : '运行 Benchmark'}</button>
            </div>
          </section>

          <div className="space-y-4 lg:col-span-2">
            <AgentPanel result={result} />
            <EvalPanel benchmark={benchmark} />
          </div>
        </div>
      </div>
    </main>
  )
}
