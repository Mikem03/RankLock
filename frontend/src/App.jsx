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
      <h1>RankLock</h1>
      <p>{message}</p>
      <HeroStats />
    </div>
  );
}

export default App;
