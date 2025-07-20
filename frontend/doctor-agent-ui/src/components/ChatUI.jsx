import { useEffect, useRef, useState } from 'react'
import '../styles/chat.css'

function ChatUI({ user }) {
  const [messages, setMessages] = useState([
    { sender: 'agent', text: 'Hi! How can I assist you today?' }
  ])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)
  const chatEndRef = useRef(null)

  const scrollToBottom = () => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  const sendMessage = async () => {
    if (!input.trim()) return

    const userMessage = { sender: 'user', text: input }
    setMessages((prev) => [...prev, userMessage])
    setInput('')
    setLoading(true)

    // Show typing indicator
    setMessages((prev) => [...prev, { sender: 'agent', text: '__typing__' }])

    try {
      const res = await fetch('http://localhost:8001/agent', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          query: input,
          session_id: 'aswin-session',
          email: user.email,
          role: user.role
        })
      })

      const data = await res.json()
      const agentMessage = {
        sender: 'agent',
        text: data.response?.output || data.response || 'No response'
      }

      setMessages((prev) =>
        [...prev.filter((m) => m.text !== '__typing__'), agentMessage]
      )
    } catch (err) {
        console.error("⚠️ Agent API error:", err)
        setMessages((prev) =>
          [...prev.filter((m) => m.text !== '__typing__'), {
            sender: 'agent',
            text: '⚠️ Failed to reach the agent API.'
          }]
        )
      }finally {
      setLoading(false)
    }
  }

  const handleKeyDown = (e) => {
    if (e.key === 'Enter') sendMessage()
  }

  return (
    <div className="chat-container">
      <div className="chat-header">🧠 Doctor Assistant</div>

      <div className="chat-box">
        {messages.map((msg, idx) => (
          <div
            key={idx}
            className={`bubble ${msg.sender} ${msg.text === '__typing__' ? 'typing' : ''}`}
          >
            {msg.text === '__typing__' ? 'Agent is thinking...' : msg.text}
          </div>
        ))}
        <div ref={chatEndRef} />
      </div>

      <div className="chat-input">
        <input
          type="text"
          placeholder="Ask something..."
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKeyDown}
          disabled={loading}
        />
        <button onClick={sendMessage} disabled={loading}>
          {loading ? '...' : 'Send'}
        </button>
      </div>
    </div>
  )
}

export default ChatUI
