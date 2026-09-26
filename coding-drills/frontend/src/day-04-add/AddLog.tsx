import { useState, useEffect } from 'react'

interface LogEntry {
  id: number
  message: string
}

export default function AddLog() {
  const [logs, setLogs] = useState<LogEntry[]>([])
  const [loading, setLoading] = useState(true)
  const [text, setText] = useState('')

  useEffect(() => {
    const load = async () => {
      const res = await fetch('http://localhost:8000/logs')
      const data = await res.json()
      setLogs(data)
      setLoading(false)
    }
    load()
  }, [])

  const addLog = async () => {
    const res = await fetch('http://localhost:8000/logs', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message: text }),
    })

    const newLog = await res.json()
    setLogs([...logs, newLog])
    setText('')
  }

  if (loading) return <p>Loading....</p>

  return (
    <div>
      <input
        value={text}
        onChange={(e) => {
          setText(e.target.value)
        }}
      />
      <button onClick={addLog}>Add</button>
      <ul>
        {logs.map((log) => (
          <li key={log.id}>{log.message}</li>
        ))}
      </ul>
    </div>
  )
}
