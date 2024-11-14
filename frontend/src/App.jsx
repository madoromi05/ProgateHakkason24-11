import { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import reactLogo from './assets/react.svg';
import viteLogo from '/vite.svg';
import rokuonnImage from './assets/rokuonn.png';
import './App.css';

function App() {
  const [isRecording, setIsRecording] = useState(false);
  const mediaRecorderRef = useRef(null);
  const socketRef = useRef(null);
 
  useEffect(() => {
    // WebSocketの接続
    socketRef.current = new WebSocket('http://127.0.0.1:5000/'); // バックエンドのURLに置き換えてください

    socketRef.current.onopen = () => {
      console.log('WebSocket connection established');
    };

    socketRef.current.onclose = () => {
      console.log('WebSocket connection closed');
    };

    return () => {
      // クリーンアップ
      socketRef.current.close();
    };
  }, []);

  const handleRecordingClick = async () => {
    if (isRecording) {
      // 録音停止
      mediaRecorderRef.current.stop();
      setIsRecording(false);
    } else {
      // 録音開始
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      mediaRecorderRef.current = new MediaRecorder(stream);

      mediaRecorderRef.current.ondataavailable = (event) => {
        if (socketRef.current && socketRef.current.readyState === WebSocket.OPEN) {
          // 音声データを送信
          socketRef.current.send(event.data);
        }
      };

      mediaRecorderRef.current.start();
      setIsRecording(true);
    }
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