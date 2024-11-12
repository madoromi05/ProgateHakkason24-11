import { useState, useEffect, useRef } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'

function App() {
  const [count, setCount] = useState(0)
  const [isRecording, setIsRecording] = useState(false);
  const [audioStream, setAudioStream] = useState(null);
  const mediaRecorderRef = useRef(null);
  const socketRef = useRef(null);
  const websocketURL = ""; // WebSocketのURL。必要であれば設定

  useEffect(() => {
    initMicrophone();
  }, []);

  async function initMicrophone() {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      setAudioStream(stream);
      console.log("マイクのアクセスが許可されました");
    } catch (error) {
      console.error("マイクへのアクセスが拒否されました:", error);
    }
  }

  function startWebSocket() {
    if (websocketURL) {
      socketRef.current = new WebSocket(websocketURL);

      socketRef.current.onopen = () => {
        console.log("WebSocket接続が開かれました");
      };

      socketRef.current.onerror = (error) => {
        console.error("WebSocketエラー:", error);
      };

      socketRef.current.onclose = () => {
        console.log("WebSocket接続が閉じられました");
      };
    } else {
      console.warn("WebSocket URLが設定されていないため、データは送信されません。");
    }
  }

  function startRecording() {
    if (audioStream) {
      mediaRecorderRef.current = new MediaRecorder(audioStream);

      mediaRecorderRef.current.ondataavailable = (event) => {
        if (event.data.size > 0 && socketRef.current && socketRef.current.readyState === WebSocket.OPEN) {
          socketRef.current.send(event.data);
        }
      };

      mediaRecorderRef.current.start();
      setIsRecording(true);
    } else {
      console.error("マイクが初期化されていないため、録音を開始できません。");
    }
  }

  function stopRecording() {
    if (mediaRecorderRef.current && mediaRecorderRef.current.state === "recording") {
      mediaRecorderRef.current.stop();
    }
    if (socketRef.current && socketRef.current.readyState === WebSocket.OPEN) {
      socketRef.current.close();
    }
    setIsRecording(false);
  }

  function handleRecordStart() {
    startWebSocket();
    startRecording();
  }

  return (
    <>
      <div>
        <a href="https://vite.dev" target="_blank">
          <img src={viteLogo} className="logo" alt="Vite logo" />
        </a>
        <a href="https://react.dev" target="_blank">
          <img src={reactLogo} className="logo react" alt="React logo" />
        </a>
      </div>
      <h1>Vite + React</h1>
      <div className="card">
        <button onClick={() => setCount((count) => count + 1)}>
          count is {count}
        </button>
        <p>
          Edit <code>src/App.jsx</code> and save to test HMR
        </p>
      </div>
      <p className="read-the-docs">
        Click on the Vite and React logos to learn more
      </p>
      <img
        className="rokuonnB"
        src="/path/to/your/image.png"
        alt="録音ボタン"
        onMouseDown={handleRecordStart}
        onMouseUp={stopRecording}
        onTouchStart={handleRecordStart}
        onTouchEnd={stopRecording}
      />
      {isRecording && <div id="recordingStatus">録音中...</div>}
    </>
  )
}

export default App