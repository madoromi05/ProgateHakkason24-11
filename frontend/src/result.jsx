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
  // 必要に応じて他のクイズ問題を追加
];

function Result() {
  const [songs, setSongs] = useState([]);
  const [currentQuiz, setCurrentQuiz] = useState(null);
  const [selectedAnswer, setSelectedAnswer] = useState(null);
  const [isCorrect, setIsCorrect] = useState(null);
  const [score, setScore] = useState(0);
  const [quizIndex, setQuizIndex] = useState(0);
  const [quizFinished, setQuizFinished] = useState(false);

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
      <ul>
        {songs.map((song, index) => (
          <li key={index}>
            {song.name} - {song.artist}
          </li>
        ))}
      </ul>

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
        <button className="next-button" onClick={nextQuiz}>次の問題へ</button>
      </div>
    )}
  </div>
)}

{quizFinished && (
  <div>
    <p>全てのクイズが終了しました！</p>
    <button className="reset-button" onClick={resetQuiz}>もう一度挑戦</button>
  </div>
)}

      <div className="button-container">
        <button className="bright-button" onClick={() => window.location.href='../index.html'}>
          もう一度計測する
        </button>
      </div>
    </div>
  );
}

export default Result;

// ReactDOMでレンダリング
import { createRoot } from 'react-dom/client';

const rootElement = document.getElementById('root');
const root = createRoot(rootElement);
root.render(<Result />);