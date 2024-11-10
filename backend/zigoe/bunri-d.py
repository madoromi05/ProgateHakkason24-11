import subprocess

# 音源分離する音声ファイルのパス
audio_file = 'testdata.mp3'

# Demucsを使って音源分離を実行
subprocess.run(['demucs', audio_file])
