import React, { useState, useEffect } from 'react';
import './App.css';

// 配列をシャッフルする関数
const shuffleArray = (array) => {
  return array.sort(() => Math.random() - 0.5);
};

// クイズデータを定義
const quizData = [
  {
    lyrics: "簡単:青に似たすっぱい春とライラック君を待つよここでね",
    options: ["ライラック", "青と夏", "ケセラセラ", "コロンブス"],
    correctAnswer: "ライラック",
  },
  {
    lyrics: "超難問:Выходила на берег Катюша,На высокий берег на крутой.",
    options: ["Варяг", "Армия моя", "Катюша", "Кукушка"],
    correctAnswer: "Катюша",
  },
  {
    lyrics: "難問:誰かが言った　いつか溜息は夜に化けて歌を歌う",
    options: ["シャルル", "ダーリン", "雨とペトラ", "ノマド"],
    correctAnswer: "雨とペトラ",
  },
  {
    lyrics: "難問:もう一回　もう一回「私は今日も転がります」と",
    options: ["ロンリーガール", "裏表ラバーズ", "アンノウン・マザーグース", "アンハッピーリフレイン"],
    correctAnswer: "ロンリーガール",
  },
  {
    lyrics: "超難問:ひらりはらり女の子ふわりふわり言葉のsaw",
    options: ["モエチャッカファイア", "はろー。", "しあわせレストラン", "さよならバースデー"],
    correctAnswer: "モエチャッカファイア",
  },
  {
    lyrics: "簡単:hihihiA hihihiB hihihiC D E",
    options: ["高音厨音域テスト", "低音厨音域テスト", "活舌厨早口テスト", "調音厨肺活量テスト"],
    correctAnswer: "高音厨音域テスト",
  },
  {
    lyrics: "簡単:J'aime l'oignon frît à l'huile,J'aime l'oignon quand il est bon",
    options: ["La Chanson de l'oignon", "Alouette", "L'Amour Est Bleu", "Les feuilles mortes"],
    correctAnswer: "La Chanson de l'oignon",
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
  const [sortOption, setSortOption] = useState('None');
  const [artistFilter, setArtistFilter] = useState('All');
  const [isAllSelected, setIsAllSelected] = useState(false);
  const [selectedSongs, setSelectedSongs] = useState([]);
  const artistOptions = ['All', ...new Set(songs.map((song) => song.artist))];
  const [shuffledQuizData, setShuffledQuizData] = useState([]); // シャッフルされたクイズデータ

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
  
    // クイズデータを一度だけシャッフルして保存
    const shuffledData = shuffleArray([...quizData]);
    setShuffledQuizData(shuffledData);
    setCurrentQuiz({ ...shuffledData[quizIndex], options: shuffleArray([...shuffledData[quizIndex].options]) });
  }, []);
  
  useEffect(() => {
    // クイズインデックスが変更されたときのみ、次のクイズを設定
    if (shuffledQuizData.length > 0) {
      setCurrentQuiz({ ...shuffledQuizData[quizIndex], options: shuffleArray([...shuffledQuizData[quizIndex].options]) });
    }
  }, [quizIndex, shuffledQuizData]);

  const handleSelectAll = () => {
    const newIsAllSelected = !isAllSelected;
    setIsAllSelected(newIsAllSelected);
    if (newIsAllSelected) {
      setSelectedSongs(filteredSongs.map((song) => song.name));
    } else {
      setSelectedSongs([]);
    }
  };

  const handleCheckboxChange = (songName) => {
    if (selectedSongs.includes(songName)) {
      // チェックを外す
      setSelectedSongs(selectedSongs.filter((name) => name !== songName));
    } else {
      // チェックを付ける
      setSelectedSongs([...selectedSongs, songName]);
    }
  };

  const handleSearch = () => {
    setSearchQuery('');
    window.location.href = '../index.html';
  };

  const handleArtistFilterChange = (artist) => {
    setArtistFilter(artist);
  };

  const handleSortChange = (option) => {
    setSortOption(option);
    let sortedSongs = [...songs];
    if (option === 'Artist') {
      sortedSongs.sort((a, b) => a.artist.localeCompare(b.artist, 'ja'));
    } else if (option === 'Title') {
      sortedSongs.sort((a, b) => a.name.localeCompare(b.name, 'ja'));
    }
    setSongs(option === 'None' ? songs : sortedSongs);
  };

  const filteredSongs = songs
  .filter((song) =>
    song.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
    song.artist.toLowerCase().includes(searchQuery.toLowerCase())
  )
  .filter((song) => (artistFilter === 'All' ? true : song.artist === artistFilter));

  const handleAnswerSelect = (answer) => {
    setSelectedAnswer(answer);
    const correct = answer === currentQuiz.correctAnswer;
    setIsCorrect(correct);
    if (correct) {
      setScore((prevScore) => prevScore + 1);
    }
  };

  const nextQuiz = () => {
    if (quizIndex < quizData.length - 1) {
      setQuizIndex((prevIndex) => prevIndex + 1);
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
        {/* 空白のヘッダー行 */}
        <div className="issue-card">
          <div className="song-info">
            {/* 一括選択チェックボックス */}
            <input
              type="checkbox"
              className="song-checkbox"
              checked={isAllSelected}
              onChange={handleSelectAll}
            />
            <span>すべて選択</span>

            {/* Sort by ドロップダウンメニューを同じ横列に配置 */}
            <div className="sort-container">
            <select
              className="artist-dropdown"
              value={artistFilter}
              onChange={(e) => handleArtistFilterChange(e.target.value)}
            > 
              {artistOptions.map((artist, index) => (
                <option key={index} value={artist}>
                  {artist}
                </option>
              ))}
            </select>
            </div>
              <select
                className="sort-dropdown"
                value={sortOption}
                onChange={(e) => handleSortChange(e.target.value)}
              >
                <option value="None">None</option>
                <option value="Artist">Artist</option>
                <option value="Title">Title</option>
              </select>
            <div className="text-info">
              <p className="song-title"></p>
              <p className="song-artist"></p>
            </div>
          </div>
        </div>

        {filteredSongs.map((song, index) => (
          <div key={index} className="issue-card">
            <div className="song-info">
              {/* 個別のチェックボックス */}
              <input
                type="checkbox"
                className="song-checkbox"
                checked={selectedSongs.includes(song.name)}
                onChange={() => handleCheckboxChange(song.name)}
              />
              <span className="status-icon"></span>
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
