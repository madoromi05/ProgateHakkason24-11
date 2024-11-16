from flask import Flask, render_template,jsonify
from flask_cors import CORS
from flask_socketio import SocketIO,emit
from pydub import AudioSegment
from recommend_songs import get_recommended_songs
import numpy as np
import os
import io

app = Flask(__name__)
CORS(app)  # すべてのオリジンからのアクセスを許可
socketio = SocketIO(app, cors_allowed_origins="*")

@app.route('/cors')
def hello():
    return 'Hello, CORS!'

@app.route('/api/recommendations', methods=['GET'])  # recommend.pyと同じエンドポイント
def get_tracks():
    try:
        recommended_songs = get_recommended_songs() # recommend.pyの関数を呼び出す
        songs_info = [
            {
                "name": song['name'],
                "artist": song['artist'],
            }
            for song in recommended_songs
        ]
        return jsonify(songs_info)

    except Exception as e:
        return jsonify({"error": f"Failed to get recommendations: {e}"}), 500

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
    audio = AudioSegment.from_file(io.BytesIO(data), format="wav")
    samples = np.array(audio.get_array_of_samples())  # 音声データをNumPy配列に変換
    emit('message', {'data': 'Audio received successfully!'})

if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)