import { useState } from 'react'

function Login({ onLogin }) {
  const [email, setEmail] = useState('')
  const [role, setRole] = useState('patient')

  const handleSubmit = (e) => {
    e.preventDefault()
    if (!email.trim()) return alert("Email is required")
    onLogin({ email, role })
  }

  return (
    <form onSubmit={handleSubmit} style={{ textAlign: 'center', marginTop: '2rem' }}>
      <h2>Login</h2>
      <select value={role} onChange={(e) => setRole(e.target.value)}>
        <option value="patient">Patient</option>
        <option value="doctor">Doctor</option>
      </select>
      <br /><br />
      <input
        type="email"
        placeholder="Enter your email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        style={{ padding: '0.5rem' }}
      />
      <br /><br />
      <button type="submit">Login</button>
    </form>
  )
}

export default Login
