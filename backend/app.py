from flask import Flask, render_template,jsonify
from flask_cors import CORS
from flask_socketio import SocketIO, emit
#from pydub import AudioSegment
from recommend_songs import get_recommended_songs
#from zigoe.test import zigoe
#from spotfyapi.test import spotfyapi
import os
import io
import numpy as np
'''
def spotfyapi(data):
    return "これで{"+data+"}よさそう"

def zigoe():
    return "受信成功"
'''
app = Flask(__name__, template_folder=os.path.join(os.path.dirname(__file__), '../frontend'))
socketio = SocketIO(app, async_mode='threading')
CORS(app)  # すべてのオリジンからのアクセスを許可
websocket_result=None
'''
@app.route('/')
def hello():
    return 'Hello, CORS!'
'''
#曲リストGET
@app.route('/tracks', methods=['GET'])
def get_tracks():
    try:
        print("recommended_call")
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

'''
def save_audio(data, filename="received_audio.wav"):
    audio = AudioSegment.from_file(io.BytesIO(data), format="wav")
    audio.export(filename, format="wav")

    #ここで呼び出し
    websocket_result=zigoe(audio)

@socketio.on('audio')
def handle_audio(data):
    print('音声データを受信しました')
    save_audio(data)

# サーバー終了時にファイルを閉じる
@socketio.on('disconnect')
def disconnect():
    print("クライアントが切断されました")
'''
if __name__ == '__main__':
    app.run(debug=True)
