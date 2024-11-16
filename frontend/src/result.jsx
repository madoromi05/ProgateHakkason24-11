import React, { useState, useEffect } from 'react';
import './App.css';

// クイズデータを直接コンポーネント内で定義
const quizData = [
  {
    lyrics: "青に似たすっぱい春とライラック君を待つよここでね",
    options: ["ライラック", "青と夏", "ケセラセラ", "コロンブス"],
    correctAnswer: "ライラック"
  },
  {
    lyrics: "ねえ　今でも覚えてる？あの日の空の色",
    options: ["青と夏", "ハルノヒ", "シーソーゲーム", "夏色"],
    correctAnswer: "青と夏"
  },
  // 必要に応じて他のクイズ問題を追加
];

function Result() {
  const [currentQuiz, setCurrentQuiz] = useState(null);
  const [selectedAnswer, setSelectedAnswer] = useState(null);
  const [isCorrect, setIsCorrect] = useState(null);

  useEffect(() => {
    // ランダムにクイズを選択
    const randomQuiz = quizData[Math.floor(Math.random() * quizData.length)];
    setCurrentQuiz(randomQuiz);
  }, []);

  const handleAnswerSelect = (answer) => {
    setSelectedAnswer(answer);
    setIsCorrect(answer === currentQuiz.correctAnswer);
  };

  return (
    <div className="Result">
      <h1>あなたにオススメの曲は!!</h1>
      {/* 推奨曲のリストはここに後で追加されます */}
      
      <div className="button-container">
        <button className="bright-button" onClick={() => window.location.href='../index.html'}>
          もう一度計測する
        </button>
      </div>
      
      {currentQuiz && (
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
            <p>{isCorrect ? '正解です！' : '不正解です。正解は ' + currentQuiz.correctAnswer + ' でした。'}</p>
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