import { useEffect, useState } from 'react'
import MainContainer from './components/MainContainer';
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
      <h1 className="main-header">RankLock</h1>
      <MainContainer />
    </div>
  );
}

export default App;
