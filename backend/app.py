from flask import Flask, render_template,jsonify
from flask_cors import CORS
from flask_socketio import SocketIO, emit
from pydub import AudioSegment
#from recommend_songs import get_recommended_songs
#from zigoe.test import zigoe
#from spotfyapi.test import spotfyapi
import io
import numpy as np

def spotfyapi(data):
    return "これで{"+data+"}よさそう"

def zigoe():
    return "受信成功"

app = Flask(__name__)
CORS(app)  # すべてのオリジンからのアクセスを許可
socketio = SocketIO(app)
websocket_result=None

@app.route('/')
def hello():
    return 'Hello, CORS!'
@app.route('/test', methods=['GET'])
def test():
    pass
@app.route('/tracks', methods=['GET'])
def get_tracks():
    try:
    # 推薦曲リストを取得
        recommended_songs = get_recommended_songs()
        #確認LOG
        if recommended_songs:
            print("曲のリストが正常に取得できました:")
            for i, song in enumerate(recommended_songs, 1):
                print(f"{i}. {song['name']} by {song['artist']}")
        else:
            print("曲のリストが取得できませんでした。")
        # 曲情報をレスポンス用に準備
        songs_info = [
            {
                "name": song['name'],
                "artist": song['artist'],
            }
            for song in recommended_songs
        ]
        return jsonify(songs_info)  # JSONとして返す
    except Exception as e:
        print(f"エラーが発生しました: {e}")  # エラーログを出力
        return jsonify({"error": "曲の取得に失敗しました。"}), 500 

def save_audio(data, filename="received_audio.wav"):
    audio = AudioSegment.from_file(io.BytesIO(data), format="wav")
    audio.export(filename, format="wav")

    #ここで呼び出し
    websocket_result=zigoe(audio)

import scipy.io.wavfile as wav
@socketio.on('audio')
def handle_audio(data):
    print('音声データを受信しました')
    save_audio(data)
    wav.write("output.wav",44100,data)

# サーバー終了時にファイルを閉じる
@socketio.on('disconnect')
def disconnect():
    print("クライアントが切断されました")

if __name__ == '__main__':
    app.run(debug=True)
