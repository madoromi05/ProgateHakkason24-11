from flask import Flask, render_template,jsonify
from flask_cors import CORS
from flask_socketio import SocketIO,emit
from pydub import AudioSegment
import numpy as np
import wave
from zigoe import zigoe_async,topng_async,topitchpng_async,tosepartionpng_async
import asyncio
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


@socketio.on('disconnect')
def handle_disconnect():
    print("Client disconnected")
@socketio.on('message_from_client')
def handle_message(data):
    print("Received message:", data)
    emit('message_from_server', {'response': 'Message received'}, broadcast=True)
@socketio.on('connect')
def handle_connect():
    print('Client connected')
    emit('message', {'data': 'Welcome to the WebSocket Audio server!'})
@socketio.on('audio_data')
def handle_audio_data(data):
    print(f"Received audio data, size: {len(data)} bytes")
    audio_ = AudioSegment.from_file(io.BytesIO(data))#
    audio=np.array(audio_.get_array_of_samples())
    emit('message', {'data': 'Audio received successfully!'})
    asyncio.run(topng_async(audio))
    print("end1")
    asyncio.run(tosepartionpng_async(audio))
    print("end2")
    asyncio.run(topitchpng_async(audio))
    print("end3")


if __name__ == '__main__':
    app.run(debug=True)
