import librosa
import numpy as np

def analyze_pitch(audio_file):
    # 音声ファイルの読み込み
    y, sr = librosa.load(audio_file)
    
    # ピッチ抽出
    pitches, magnitudes = librosa.piptrack(y=y, sr=sr)
    
    # 有効なピッチの平均を計算
    pitches_filtered = pitches[pitches > 0]
    avg_pitch = np.mean(pitches_filtered)
    
    # 声域の判定
    if avg_pitch < 85:
        return "低音部 (Bass)"
    elif 85 <= avg_pitch < 165:
        return "バリトン (Baritone)"
    elif 165 <= avg_pitch < 255:
        return "テノール (Tenor)"
    elif 255 <= avg_pitch < 350:
        return "アルト (Alto)"
    elif 350 <= avg_pitch < 525:
        return "ソプラノ (Soprano)"
    else:
        return "超高音域"

# 使用例
audio_file = r"separated\htdemucs\752912460.876488\vocals.wav"
voice_range = analyze_pitch(audio_file)
print(f"推定される声域: {voice_range}")