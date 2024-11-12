import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd

# Spotify API認証
client_id = '20e9a4be685749e2bf74fa422a90ee77'
client_secret = 'c2ebbce0ad1d4b43b086e377fa1368f5'

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=client_id, client_secret=client_secret))

# ユーザーの声域データ
user_lowest_pitch = float(input("あなたの最低音をHz単位で入力してください（例: 130）: "))
user_highest_pitch = float(input("あなたの最高音をHz単位で入力してください（例: 523）: "))

# キーと音程の対応表
key_pitch_map = {
    0: 261.63, 1: 277.18, 2: 293.66, 3: 311.13, 4: 329.63,
    5: 349.23, 6: 369.99, 7: 392.00, 8: 415.30, 9: 440.00,
    10: 466.16, 11: 493.88
}

def pitch_in_range(track_key, track_mode):
    base_pitch = key_pitch_map[track_key]
    if track_mode == 0:  # マイナーキーの場合
        base_pitch *= 0.9
    return user_lowest_pitch <= base_pitch <= user_highest_pitch

def recommend_japanese_songs(limit=20):
    recommended_tracks = []
    offset = 0

    while len(recommended_tracks) < limit:
        # 日本市場に限定して検索
        results = sp.search(q='year:2020-2023', type='track', limit=30, offset=offset, market='JP')

        for track in results['tracks']['items']:
            if len(recommended_tracks) >= limit:
                break

            track_id = track['id']
            features = sp.audio_features(track_id)[0]

            if features and pitch_in_range(features['key'], features['mode']):
                recommended_tracks.append({
                    'name': track['name'],
                    'artist': track['artists'][0]['name'],
                })

        offset += 20
        if len(results['tracks']['items']) < 20:
            break

    return recommended_tracks

# 推薦曲の取得と表示
def get_recommended_songs():
    return recommend_japanese_songs()