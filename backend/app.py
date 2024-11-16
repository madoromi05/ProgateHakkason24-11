from flask import Flask, render_template,jsonify, request
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
import uuid
datadict:dict[str,dict]={}
app = Flask(__name__)
CORS(app)  # すべてのオリジンからのアクセスを許可
socketio = SocketIO(app, async_mode='threading', cors_allowed_origins="*")

@app.route('/cors')
def hello():
    return 'Hello, CORS!'

@app.route('/api/recommendations', methods=['GET'])
def get_recommendations():
    try:
        id = request.remote_addr
        return app.response_class(
            response=jsonify(datadict[id]).data.decode("utf-8"),
            content_type="application/json; charset=utf-8",
        )
    except Exception as e:
        print(f"Failed to get recommendations: {e}")
        return jsonify({"error": f"Failed to get recommendations: {e}"}), 500



@socketio.on('disconnect')
def handle_disconnect():print("Client disconnected")
@socketio.on('connect')
def handle_connect():
    print('Client connected')
@socketio.on('connection')
def handle_connect():print('Clien connection')

@socketio.on('audio_data')
def handle_audio_data(data):
    try:
        id = request.remote_addr
        print(datadict)
        print(f"Received audio data, size: {len(data)} bytes")
        audio_ = AudioSegment.from_file(io.BytesIO(data))
        audio=np.array(audio_.get_array_of_samples())
        pitch=asyncio.run(zigoe_async(audio))
        datadict[id] = get_recommended_songs(user_lowest_pitch=pitch["min"], user_highest_pitch=pitch["max"], limit=30)
        print(pitch)
    except Exception as e:
        print(f"Failed to get recommendations: {e}")
        return socketio.emit({"status": 'error',"code": 500,"message":f"Failed to get recommendations: {e}",
})

if __name__ == '__main__':
    app.run(debug=True)
