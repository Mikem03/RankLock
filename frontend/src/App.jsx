import { useEffect, useState } from 'react'
import HeroStats from './components/HeroStats';
import './index.css'

function App() {
  const [message, setMessage] = useState('Loading...')


  useEffect(() => {
    fetch('http://localhost:5000/api/message')
      .then((response) => response.json())
      .then((data) => setMessage(data.message))
      .catch((error) => {
        console.error('Error fetching message:', error)
        setMessage('Failed to load message')
      })
  }, [])

  return (
    <div className='App'>
      <img src="/logo.png" alt="RankLock Logo" className="logo" />
      <h1>RankLock</h1>
      <HeroStats />
    </div>
  );
}

export default App;
