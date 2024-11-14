import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
from flask import Flask, jsonify

# Spotify API認証
client_id = '20e9a4be685749e2bf74fa422a90ee77'
client_secret = 'c2ebbce0ad1d4b43b086e377fa1368f5'

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=client_id, client_secret=client_secret))

# ユーザーの声域データ,testのために固定
user_lowest_pitch = 130
user_highest_pitch = 523

# キーと音程の対応表
key_pitch_map = {
    0: 261.63, 1: 277.18, 2: 293.66, 3: 311.13, 4: 329.63,
    5: 349.23, 6: 369.99, 7: 392.00, 8: 415.30, 9: 440.00,
    10: 466.16, 11: 493.88
}

def pitch_in_range(track_key, track_mode, user_lowest_pitch, user_highest_pitch):
    base_pitch = key_pitch_map[track_key]
    if track_mode == 0:  # マイナーキーの場合
        base_pitch *= 0.9
    return user_lowest_pitch <= base_pitch <= user_highest_pitch

def get_recommended_songs(user_lowest_pitch, user_highest_pitch, limit=30):
    recommended_tracks = []
    offset = 0

    while len(recommended_tracks) < limit:
        #日本市場100曲から30曲選ぶ
        results = sp.search(q='year:2020-2023', type='track', limit=100, offset=offset, market='JP') # limitを大きくして検索効率アップ

        for track in results['tracks']['items']:
            if len(recommended_tracks) >= limit:
                break

            track_id = track['id']
            try: # API呼び出しエラーをtry-exceptで処理
                features = sp.audio_features(track_id)[0]
                if features and pitch_in_range(features['key'], features['mode'], user_lowest_pitch, user_highest_pitch):
                    recommended_tracks.append({
                        'name': track['name'],
                        'artist': track['artists'][0]['name'],
                    })
            except Exception as e:
                print(f"Error getting audio features for track {track_id}: {e}")

        offset += 100
        if not results['tracks']['items']: # 検索結果が空ならループを抜ける
            break

    return recommended_tracks