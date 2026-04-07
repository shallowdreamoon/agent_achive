export default function AgentPanel({ runResult }) {
  if (!runResult) return null

  return (
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
  )
}
