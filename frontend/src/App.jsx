import React, { useState } from 'react';
import io from 'socket.io-client';

const socket = io('http://localhost:5000'); // FlaskサーバーのURL

function App() {
  const [isRecording, setIsRecording] = useState(false);
  const [mediaRecorder, setMediaRecorder] = useState(null);

  const startRecording = async () => {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    const recorder = new MediaRecorder(stream);
    recorder.ondataavailable = (event) => {
      if (event.data.size > 0) {
        sendAudioData(event.data);
      }
    };
    recorder.start();
    setMediaRecorder(recorder);
    setIsRecording(true);
  };

  const stopRecording = () => {
    if (mediaRecorder) {
      mediaRecorder.stop();
      setIsRecording(false);
    }
  };

  const sendAudioData = (audioBlob) => {
    const reader = new FileReader();
    reader.onload = () => {
      const arrayBuffer = reader.result;
      socket.emit('audio_data', arrayBuffer);
    };
    reader.readAsArrayBuffer(audioBlob);
  };

  return (
    <div>
      <h1>Record and Send Audio</h1>
      <button onClick={startRecording} disabled={isRecording}>
        Start Recording
      </button>
      <button onClick={stopRecording} disabled={!isRecording}>
        Stop Recording
      </button>
    </div>
  );
}

export default App;
