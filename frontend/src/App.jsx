import { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import reactLogo from './assets/react.svg';
import viteLogo from '/vite.svg';
import rokuonnImage from './assets/rokuonn.png';
import './App.css';
import { io } from 'socket.io-client';

function App() {
  const [isRecording, setIsRecording] = useState(false);
  const mediaRecorderRef = useRef(null);
 
  
  const socket = io('http://localhost:' + 5000);
  socket.on("connection", (socket) => {console.log(socket.id)});
  socket.on("connect", () => {console.log(socket.id)});
  socket.on("disconnect", () => {console.log(socket.id)});

  const handleRecordingClick = async () => {
    if (isRecording) {
      // 録音停止
      mediaRecorderRef.current.stop();
      setIsRecording(false);
    } else {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      mediaRecorderRef.current = new MediaRecorder(stream);

      mediaRecorderRef.current.ondataavailable = (event) => {
        if (event.data.size > 0) {
          console.log(event.data.length)
          sendAudioData(event.data);
        }
      };
      mediaRecorderRef.current.start();
      setIsRecording(true);
    }
  };
  const sendAudioData = (audioBlob) => {
    // BlobをArrayBufferに変換して送信
    const reader = new FileReader();
    reader.onload = () => {
      const arrayBuffer = reader.result;
      socket.emit('audio_data', arrayBuffer); // サーバーに音声データを送信
    };
    reader.readAsArrayBuffer(audioBlob);
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
      <div style={{ height: '30px', marginTop: '10px' }}>
        {isRecording && <p className="recording-text">録音中</p>}
      </div>
      <div className="result_button">
        <a href="./result.html">結果を見る</a>
      </div>
    </div>
  );
}

export default App;