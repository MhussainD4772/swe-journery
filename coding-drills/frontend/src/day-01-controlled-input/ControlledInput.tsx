import { useState } from 'react'

export default function ControlledInput() {
  const [text, setText] = useState('')
  return (
    <div>
      <input
        value={text}
        onChange={(e) => {
          setText(e.target.value)
        }}
      />
      <p>{text}</p>
    </div>
  )
}
