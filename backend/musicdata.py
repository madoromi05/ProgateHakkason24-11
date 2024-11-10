from flask import Flask, jsonify
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# Flaskアプリケーションのインスタンスを作成
app = Flask(__name__)

# Spotify APIのクライアントIDとクライアントシークレットを設定
client_id = '20e9a4be685749e2bf74fa422a90ee77'
client_secret = 'c2ebbce0ad1d4b43b086e377fa1368f5'

# Spotify APIへの認証を設定
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=client_id, client_secret=client_secret))

# トラック情報を取得するエンドポイントを定義
@app.route('/tracks', methods=['GET'])

def get_tracks():
    # Spotify APIを使って「Imagine」に関連するトラックを検索
    results = sp.search(q='Imagine', type='track', limit=10)

    # トラック情報を格納するリストを初期化
    tracks = []

    # 検索結果からトラック情報を抽出
    for track in results['tracks']['items']:
        # アーティスト名が存在する場合は取得し、なければ「Unknown Artist」とする
        artist_name = track['artists'][0]['name'] if track['artists'] else "Unknown Artist"
        # トラック名とアーティスト名を辞書形式でリストに追加
        tracks.append({'track': track['name'], 'artist': artist_name})

    # トラック情報のリストをJSON形式で返す?
    return jsonify(tracks)

# アプリケーションが直接実行された場合にサーバーを起動
if __name__ == '__main__':
    app.run(debug=True)  # デバッグモードでFlaskサーバーを起動s