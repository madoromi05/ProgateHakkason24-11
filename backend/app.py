from flask import Flask, render_template,jsonify
from flask_cors import CORS
from flask_socketio import SocketIO, emit
from pydub import AudioSegment
from zigoe.test import zigoe
from spotfyapi.test import spotfyapi
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
@app.route('/tracks', methods=['GET'])
def get_tracks():
    # トラック情報を格納するリストを初期化
    global websocket_result
    
    # 結果を待機（WebSocket側で処理が終わるまで待つ）
    while websocket_result is None:
        socketio.sleep(1)  # 1秒待機して再確認
    data=spotfyapi(websocket_result)
    return jsonify(data)
def save_audio(data, filename="received_audio.wav"):
    audio = AudioSegment.from_file(io.BytesIO(data), format="wav")
    audio.export(filename, format="wav")

    #ここで呼び出し
    websocket_result=zigoe(audio)
@socketio.on('audio')
def handle_audio(data):
    print('音声データを受信しました')
    save_audio(data)
@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

# サーバー終了時にファイルを閉じる
@socketio.on('disconnect')
def disconnect():
    print("クライアントが切断されました")
    
if __name__ == '__main__':
    app.run(debug=True)