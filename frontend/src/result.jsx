import React, { useState, useEffect } from 'react';
import './App.css';

// クイズデータを定義
const quizData = [
  {
    lyrics: "簡単:青に似たすっぱい春とライラック君を待つよここでね",
    options: ["ライラック", "青と夏", "ケセラセラ", "コロンブス"],
    correctAnswer: "ライラック"
  },
  {
    lyrics: "超難問:Выходила на берег Катюша,На высокий берег на крутой.",
    options: ["Варяг", "Армия моя", "Катюша", "Кукушка"],
    correctAnswer: "Катюша"
  },
  {
    lyrics: "難問:誰かが言った　いつか溜息は夜に化けて歌を歌う",
    options: ["シャルル", "ダーリン", "雨とペトラ", "ノマド"],
    correctAnswer: "雨とペトラ"
  },
];

function Result() {
  const [songs, setSongs] = useState([]);
  const [currentQuiz, setCurrentQuiz] = useState(null);
  const [selectedAnswer, setSelectedAnswer] = useState(null);
  const [isCorrect, setIsCorrect] = useState(null);
  const [score, setScore] = useState(0);
  const [quizIndex, setQuizIndex] = useState(0);
  const [quizFinished, setQuizFinished] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');

  // データの取得とクイズの初期化
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
    setCurrentQuiz(quizData[quizIndex]);
  }, [quizIndex]);

  // 曲名・作曲者の検索処理
  const handleSearch = () => {
    setSearchQuery('');
    window.location.href = '../index.html'; // 「もう一度計測する」と同じ動作に変更
  };

  // 曲名や作曲者のフィルタリング
  const filteredSongs = songs.filter((song) =>
    song.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
    song.artist.toLowerCase().includes(searchQuery.toLowerCase())
  );

  const handleAnswerSelect = (answer) => {
    setSelectedAnswer(answer);
    const correct = answer === currentQuiz.correctAnswer;
    setIsCorrect(correct);
    if (correct) {
      setScore(prevScore => prevScore + 1);
    }
  };

  const nextQuiz = () => {
    if (quizIndex < quizData.length - 1) {
      setQuizIndex(prevIndex => prevIndex + 1);
      setSelectedAnswer(null);
      setIsCorrect(null);
    } else {
      setQuizFinished(true);
    }
  };

  const resetQuiz = () => {
    setQuizIndex(0);
    setScore(0);
    setSelectedAnswer(null);
    setIsCorrect(null);
    setQuizFinished(false);
  };

  return (
    <div className="Result">
      <h1>あなたにオススメの曲は!!</h1>

      {/* Atist or Title */}
      <div className="search-container">
        <input
          type="text"
          className="search-bar"
          placeholder="Atist or Title"
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
        />
        <button className="search-button" onClick={handleSearch}>
        One more measurement
        </button>
      </div>

      <div className="recommendation-container">
        {filteredSongs.map((song, index) => (
          <div key={index} className="issue-card">
            <div className="song-info">
              <input type="checkbox" className="song-checkbox" /> {/* チェックボックスを追加 */}
              <span className="status-icon"></span> {/* アイコンを追加 */}
              <div className="text-info">  
                <p className="song-title">{song.name}</p>
                <p className="song-artist">#{song.artist}</p>
              </div>
            </div>
          </div>
        ))}
      </div>

      <div className="Score">
        <h2>クイズ合計点: {score}</h2>
      </div>

      {currentQuiz && !quizFinished && (
        <div className="Quiz">
          <h2>歌詞クイズ</h2>
          <p>{currentQuiz.lyrics}</p>
          <ul>
            {currentQuiz.options.map((option, index) => (
              <li key={index}>
                <button onClick={() => handleAnswerSelect(option)} disabled={selectedAnswer !== null}>
                  {option}
                </button>
              </li>
            ))}
          </ul>
          {selectedAnswer && (
            <div>
              <p>{isCorrect ? '正解です！' : '不正解です。正解は ' + currentQuiz.correctAnswer + ' でした。'}</p>
              {quizIndex < quizData.length - 1 ? (
                <button onClick={nextQuiz}>次の問題へ</button>
              ) : (
                <div>
                  <p>合計{score}点でした！</p>
                  <button onClick={resetQuiz}>もう一度最初から解く</button>
                </div>
              )}
            </div>
          )}
        </div>
      )}
    </div>
  );
}

export default Result;

// ReactDOMでレンダリング
import { createRoot } from 'react-dom/client';

const rootElement = document.getElementById('root');
const root = createRoot(rootElement);
root.render(<Result />);
