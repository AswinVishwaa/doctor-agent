import ChatUI from '../components/ChatUI'

function Home({ user }) {
  return (
    <div>
      <h1 style={{ textAlign: 'center' }}>🧠 Doctor Assistant</h1>
      <ChatUI user={user} />
    </div>
  )
}

export default Home
