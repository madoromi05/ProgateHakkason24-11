import React, { useState, useEffect } from 'react';
import './App.css';

function Result() { // Resultコンポーネントを定義
  const [songs, setSongs] = useState([]);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch('http://127.0.0.1:5000/api/recommendations');
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        setSongs(data);
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    };

    fetchData();
  }, []);

  return ( // Resultコンポーネント内のreturn
    <div className="Result">
      <h1>あなたにオススメの曲は!!</h1>
      <ul>
        {songs.map((song, index) => (
          <li key={index}>
            {song.name} - {song.artist}
          </li>
        ))}
      </ul>
      <div className="button-container">
        <button className="bright-button" onClick={() => window.location.href='../index.html'}>
          もう一度計測する
        </button>
      </div>
    </div>
  );
} // Resultコンポーネントの終わり

export default Result;

// ReactDOMでレンダリング
import { createRoot } from 'react-dom/client';

const rootElement = document.getElementById('root');
const root = createRoot(rootElement);
root.render(<Result />);