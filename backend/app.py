from flask import Flask, render_template,jsonify
from flask_cors import CORS
from flask_socketio import SocketIO,emit
import os
import io
def get_recommended_songs(): raise ZeroDivisionError("ee")
app = Flask(__name__, template_folder=os.path.join(os.path.dirname(__file__), '../frontend'))
CORS(app)  # すべてのオリジンからのアクセスを許可
socketio = SocketIO(app, async_mode='threading', cors_allowed_origins="*")
@app.route('/cors')
def hello():
    return 'Hello, CORS!'
#曲リストGET
@app.route('/tracks', methods=['GET'])
def get_tracks():
    try:
        print("recommended_not_coll")
        recommended_songs = get_recommended_songs() # recommend_songs.pyの関数を呼び出す
        songs_info = [
            {
                "name": song['name'],
                "artist": song['artist'],
            }
            for song in recommended_songs
        ]

        return jsonify(songs_info)

    except Exception as e:
        print(f"Error getting tracks: {e}")
        return jsonify({"error": "曲の取得に失敗しました。"}), 500

@app.route('/')
def index():  # ルートパスをindex()に変更
    try:
        recommended_songs = get_recommended_songs()
        return render_template('../frontend/template.html', songs=recommended_songs) # template.htmlにsongs変数として渡す
    except Exception as e:
        print(f"Error getting tracks: {e}")
        return "Error getting tracks", 500


# WebSocket接続時
@socketio.on('connect')
def handle_connect():
    print('Client connected')
    emit('message', {'data': 'Welcome to the WebSocket Audio server!'})

# 音声データを受信
@socketio.on('audio_data')
def handle_audio_data(data):
    print(f"Received audio data, size: {len(data)} bytes")
    
    # 受信した音声データを処理する（ここでは保存しませんが、音声処理や保存を行うことができます）
    audio_file = io.BytesIO(data)  # バイナリデータをファイルとして扱う
    with open('received_audio.wav', 'wb') as f:
        f.write(audio_file.read())
    emit('message', {'data': 'Audio received successfully!'})



if __name__ == '__main__':
    app.run(debug=True)
