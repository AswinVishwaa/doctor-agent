import { useState } from 'react'
import Home from './pages/Home'
import Login from './components/Login'

function App() {
  const [user, setUser] = useState(null)

  return user
    ? <Home user={user} />
    : <Login onLogin={setUser} />
}

export default App
