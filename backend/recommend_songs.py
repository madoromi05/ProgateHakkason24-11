import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
from flask import Flask, jsonify
from flask import Flask, render_template, jsonify
from flask_cors import CORS

app = Flask(__name__, template_folder='../frontend')

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
    print(f"Checking pitch_in_range for key: {track_key}, mode: {track_mode}")
    base_pitch = key_pitch_map[track_key]
    if track_mode == 0:  # マイナーキーの場合
        base_pitch *= 0.9
    print(f"Base pitch: {base_pitch}")
    return user_lowest_pitch <= base_pitch <= user_highest_pitch

#ここで固定しないと曲が表示されない？
def get_recommended_songs(user_lowest_pitch=130, user_highest_pitch=523, limit=30):
    recommended_tracks = []
    offset = 0
    print("Entering get_recommended_songs")

    while len(recommended_tracks) < limit:
        try:
            results = sp.search(q='year:2020-2023', type='track', limit=50, offset=offset, market='JP') # limit を 50 に減らす
            if not results['tracks']['items']:  # 結果が空かどうかを確認する
                print("tracks=NULL")
                break  # 空の場合はループを抜ける

            track_ids = [track['id'] for track in results['tracks']['items']]
            try:
                features_list = sp.audio_features(track_ids) # オーディオ機能の一括リクエスト
            except Exception as e:
                print(f"Error getting audio features: {e}")
                break # 無限ループを避けるためにエラー時にループを抜ける

            for i, track in enumerate(results['tracks']['items']):
                if len(recommended_tracks) >= limit:
                    break

                features = features_list[i]
                if features: # features が None でないことを確認する
                    if pitch_in_range(features['key'], features['mode'], user_lowest_pitch, user_highest_pitch):
                        recommended_tracks.append({
                            'name': track['name'],
                            'artist': track['artists'][0]['name'],
                        })
                else:
                    print(f"Features is None for track: {track.get('name', 'Unknown')}")

            offset += 50

        except Exception as e:
            print(f"Error during sp.search: {e}")
            return [] # 検索エラー時に空のリストを返す

    return recommended_tracks

app = Flask(__name__)
CORS(app)

@app.route('/api/recommendations')
def recommendations_api():
    try:
        songs = get_recommended_songs()
        if not songs:
            return jsonify({"error": "No songs found"}), 404
        return jsonify(songs)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
