import { useState, useEffect } from 'react'
import axios from 'axios'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import rokuonnImage from './assets/rokuonn.png'
import './App.css'
import './App.css'

function App() {
  const [message, setMessage] = useState('');
  const [isRecording, setIsRecording] = useState(false);

  useEffect(() => {
    console.log("Recording state changed:", isRecording);
  }, [isRecording]);

  const [, forceUpdate] = useState({});
  const RecordingStatus = ({ isRecording }) => (
    isRecording ? <p className="recording-text">録音中</p> : null
  );
  
  // App.jsxの中で
  <RecordingStatus isRecording={isRecording} />

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
      <div style={{height: '30px', marginTop: '10px'}}>
        {isRecording ? (
          <p className="recording-text">録音中</p>
        ) : null}
      </div>
      <div className="result_button">
        <a href="./result.html">結果を見る</a>
      </div>
    </div>
  )
}

export default App
