import React from 'react';
import './App.css'; // 必要なCSSをインポート

function Result() {
  return (
    <div className="Result">
      <h1>あなたの声は!!</h1>
      {/* 結果表示用のコンテンツをここに追加 */}
      <div className="button-container">
        <button className="bright-button" onClick={() => window.location.href='./index.html'}>
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