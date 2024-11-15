import { useState, useRef } from 'react';
import axios from 'axios';
import rokuonnImage from './assets/rokuonn.png';
import './App.css';

function App() {
  const [isRecording, setIsRecording] = useState(false);
  const [dataSent, setDataSent] = useState(0);
  const mediaRecorderRef = useRef(null);
  const chunksRef = useRef([]);

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
          if (event.data.size > 0) {
            chunksRef.current.push(event.data);
          }
        };

        mediaRecorderRef.current.onstop = async () => {
          const audioBlob = new Blob(chunksRef.current, { type: 'audio/webm' });
          const formData = new FormData();
          formData.append('audio', audioBlob, 'audio.webm');
        
          try {
            const response = await axios.post('http://127.0.0.1:5000', formData, {
              headers: {
                'Content-Type': 'multipart/form-data'
              }
            });
            console.log('音声データ送信成功:', response.data);
            setDataSent(audioBlob.size);
          } catch (error) {
            if (error.response) {
              // サーバーからのレスポンスがある場合
              console.error('サーバーエラー:', error.response.status, error.response.data);
            } else if (error.request) {
              // リクエストは送信されたがレスポンスがない場合
              console.error('リクエストエラー:', error.request);
            } else {
              // リクエストの設定中にエラーが発生した場合
              console.error('その他のエラー:', error.message);
            }
          }
        
          chunksRef.current = [];
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
        {!isRecording && dataSent > 0 && <p>送信されたデータ: {dataSent} バイト</p>}
      </div>
      <div className="result_button">
        <a href="./result.html">結果を見る</a>
      </div>
    </div>
  );
}

export default App;