interface LogEntry {
  id: number
  message: string
}

export default function List() {
  const logs: LogEntry[] = [
    { id: 1, message: 'server started' },
    { id: 2, message: 'request received' },
    { id: 3, message: 'no errors' },
  ]
  return (
    <div>
      <ul>
        {logs.map((log) => (
          <li key={log.id}>{log.message}</li>
        ))}
      </ul>
    </div>
  )
}
