import { useState, useEffect } from 'react'

interface LogEntry {
  id: number
  message: string
}

export default function Fetch() {
  const [logs, setLogs] = useState<LogEntry[]>([])
  const [loading, setLoading] = useState(true)
  useEffect(() => {
    const load = async () => {
      const res = await fetch('http://localhost:8000/logs')
      const data = await res.json()
      setLogs(data)
      setLoading(false)
    }
    load()
  }, [])

  if (loading) return <p>Loading...</p>

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
