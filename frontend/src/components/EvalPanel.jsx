export default function EvalPanel({ benchmarkResult }) {
  if (!benchmarkResult) return null

  return (
    <div style={{ border: '1px solid #ccc', padding: 12 }}>
      <div><b>benchmark summary:</b></div>
      <pre>{JSON.stringify(benchmarkResult.summary, null, 2)}</pre>
    </div>
  )
}
