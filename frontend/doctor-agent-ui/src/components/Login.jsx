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
    <div style={styles.container}>
      <form onSubmit={handleSubmit} style={styles.form}>
        <h2 style={styles.title}>Login</h2>

        <label style={styles.label}>Role:</label>
        <select value={role} onChange={(e) => setRole(e.target.value)} style={styles.select}>
          <option value="patient">Patient</option>
          <option value="doctor">Doctor</option>
        </select>

        <label style={styles.label}>Email:</label>
        <input
          type="email"
          placeholder="Enter your email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          style={styles.input}
        />

        <button type="submit" style={styles.button}>Login</button>
      </form>
    </div>
  )
}

const styles = {
  container: {
    height: '100vh',
    display: 'flex',
    justifyContent: 'center',
    alignItems: 'center',
    background: '#f4f4f4',
    fontFamily: 'Arial, sans-serif'
  },
  form: {
    backgroundColor: '#fff',
    padding: '2rem',
    borderRadius: '8px',
    boxShadow: '0 2px 10px rgba(0,0,0,0.1)',
    minWidth: '300px',
    display: 'flex',
    flexDirection: 'column',
    gap: '1rem'
  },
  title: {
    marginBottom: '1rem',
    fontSize: '1.5rem',
    color: '#333'
  },
  label: {
    fontWeight: 'bold',
    textAlign: 'left',
    color: '#555'
  },
  input: {
    padding: '0.5rem',
    borderRadius: '4px',
    border: '1px solid #ccc',
    fontSize: '1rem'
  },
  select: {
    padding: '0.5rem',
    borderRadius: '4px',
    border: '1px solid #ccc',
    fontSize: '1rem'
  },
  button: {
    padding: '0.6rem',
    border: 'none',
    borderRadius: '4px',
    backgroundColor: '#4CAF50',
    color: 'white',
    fontWeight: 'bold',
    fontSize: '1rem',
    cursor: 'pointer'
  }
}

export default Login
