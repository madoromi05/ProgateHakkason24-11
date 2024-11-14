import { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import reactLogo from './assets/react.svg';
import viteLogo from '/vite.svg';
import rokuonnImage from './assets/rokuonn.png';
import './App.css';

function App() {
  const [isRecording, setIsRecording] = useState(false);
  const [dataSent, setDataSent] = useState(0);
  const mediaRecorderRef = useRef(null);
  const socketRef = useRef(null);
 
  useEffect(() => {
    const connectWebSocket = () => {
      const ws = new WebSocket('ws://localhost:5000');
  
      ws.onopen = () => {
        console.log('WebSocket接続確立');
        socketRef.current = ws;
      };
  
      ws.onerror = (error) => {
        console.error('WebSocketエラー:', error);
      };
  
      ws.onclose = (event) => {
        console.log('WebSocket接続終了:', event.code, event.reason);
        // 再接続を試みる
        setTimeout(connectWebSocket, 3000);
      };
  
      socketRef.current = ws;
    };
  
    connectWebSocket();
  
    return () => {
      if (socketRef.current) {
        socketRef.current.close();
      }
    };
  }, []);

  const handleRecordingClick = async () => {
    if (isRecording) {
      // 録音停止
      mediaRecorderRef.current.stop();
      setIsRecording(false);
    } else {
      // 録音開始
      try {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        mediaRecorderRef.current = new MediaRecorder(stream);

        mediaRecorderRef.current.ondataavailable = (event) => {
          if (socketRef.current && socketRef.current.readyState === WebSocket.OPEN) {
            // 音声データを送信
            socketRef.current.send(event.data);
            console.log('音声データ送信:', event.data.size, 'バイト');
            setDataSent(prevData => prevData + event.data.size);
          }
        };

        mediaRecorderRef.current.start();
        setIsRecording(true);
        setDataSent(0); // 新しい録音セッションを開始するときにリセット
      } catch (error) {
        console.error('メディアデバイスへのアクセスエラー:', error);
      }
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
      <div>
        {isRecording && <p>送信されたデータ: {dataSent} バイト</p>}
      </div>
      <div className="result_button">
        <a href="./result.html">結果を見る</a>
      </div>
    </div>
  );
}

export default App;