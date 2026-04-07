export default function EvalPanel({ benchmark }) {
  if (!benchmark) {
    return null
  }

  return (
    <div style={{ border: '1px solid #ccc', padding: '12px' }}>
      <h2>Benchmark Summary</h2>
      <pre style={{ background: '#f4f4f4', padding: '8px', overflowX: 'auto' }}>
        {JSON.stringify(benchmark.summary, null, 2)}
      </pre>
    </div>
  )
}
