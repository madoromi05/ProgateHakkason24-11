import { useState, useEffect } from 'react'
import axios from 'axios'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import rokuonnImage from './assets/rokuonn.png'
import './App.css'

function App() {
  const [message, setMessage] = useState('');
  const [isRecording, setIsRecording] = useState(false);

  useEffect(() => {
    axios.get('http://localhost:5000/api/hello')
      .then(response => setMessage(response.data.message))
      .catch(error => console.error('Error:', error));
  }, []);

  const handleRecordingClick = () => {
    setIsRecording(!isRecording);
    // ここに録音の開始/停止のロジックを追加できます
  };

  return (
    <div className="App">
      <h1>音程を計測しよう!!</h1>
      <div className="img_index_recording">
        <img 
          src={rokuonnImage} 
          alt="録音"
          onClick={handleRecordingClick}
          style={{ cursor: 'pointer' }}
        />
      </div>
      {isRecording && <p className="recording-text">録音中</p>}
      <div className="result_button">
        <a href="./result.html">結果を見る</a>
      </div>
    </div>
  )
}

export default App
