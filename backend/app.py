from flask import Flask, render_template,jsonify
from flask_cors import CORS
from flask_socketio import SocketIO,emit
from pydub import AudioSegment
from recommend_songs import get_recommended_songs
import numpy as np
import wave
from zigoe import zigoe_async,topng_async,topitchpng_async,tosepartionpng_async
import asyncio
import os
import io

def get_recommended_songs(): raise ZeroDivisionError("ee")
app = Flask(__name__)
CORS(app)  # すべてのオリジンからのアクセスを許可
socketio = SocketIO(app, async_mode='threading', cors_allowed_origins="*")

@app.route('/cors')
def hello():
    return 'Hello, CORS!'

@app.route('/api/recommendations', methods=['GET'])
def get_recommendations():
    try:
        # `get_recommended_songs`を呼び出して曲データを取得
        recommended_songs = get_recommended_songs(user_lowest_pitch=130, user_highest_pitch=523, limit=30)

        # `ensure_ascii=False` を使用してUnicodeをエスケープしないようにする
        return app.response_class(
            response=jsonify(recommended_songs).data.decode("utf-8"),
            content_type="application/json; charset=utf-8",
        )
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
    audio_ = AudioSegment.from_file(io.BytesIO(data))
    audio=np.array(audio_.get_array_of_samples())
    emit('message', {'data': 'Audio received successfully!'})
    d=asyncio.run(zigoe_async(audio))
    print(d)

if __name__ == '__main__':
    app.run(debug=True)
