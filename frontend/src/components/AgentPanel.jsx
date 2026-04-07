export default function AgentPanel({ result }) {
  if (!result) {
    return null
  }

  return (
    <div style={{ border: '1px solid #ccc', padding: '12px', marginBottom: '12px' }}>
      <h2>Run Result</h2>
      <div><strong>selected_agent:</strong> {result.selected_agent}</div>
      <div><strong>routing_reason:</strong> {result.routing_reason}</div>

      <h3>structured_result</h3>
      <pre style={{ background: '#f4f4f4', padding: '8px', overflowX: 'auto' }}>
        {JSON.stringify(result.structured_result, null, 2)}
      </pre>

      <h3>evidence</h3>
      <ul>
        {(result.evidence || []).map((item, index) => (
          <li key={`${item.id || 'item'}-${index}`}>
            <div><strong>{item.title || item.id}</strong></div>
            <div>{item.snippet}</div>
          </li>
        ))}
      </ul>
    </div>
  )
}
