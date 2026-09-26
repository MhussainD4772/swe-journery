import { useState } from 'react'

export default function ControlInput() {
  const [text, settext] = useState('')
  return (
    <div>
      <input value={text} onChange={(e) => settext(e.target.value)} />
      <p>{text}</p>
    </div>
  )
}
