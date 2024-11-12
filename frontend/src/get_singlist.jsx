import React, { useEffect, useState } from 'react';

const Tracks = () => {
    const [tracks, setTracks] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchTracks = async () => {
            try {
                const response = await fetch('/tracks'); // APIのエンドポイントにリクエスト
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                const data = await response.json();
                setTracks(data); // 取得したデータを状態にセット
            } catch (error) {
                setError(error.message); // エラーメッセージを状態にセット
            } finally {
                setLoading(false); // ローディング状態を解除
            }
        };

        fetchTracks(); // データ取得関数を呼び出す
    }, []);

    if (loading) {
        return <div>Loading...</div>; // ローディング中のメッセージ
    }

    if (error) {
        return <div>Error: {error}</div>; // エラーが発生した場合のメッセージ
    }

    return (
        <div>
            <h1>Recommended Tracks</h1>
            <ul>
                {tracks.map((track, index) => (
                    <li key={index}>
                        {track.name} by {track.artist}
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default Tracks;