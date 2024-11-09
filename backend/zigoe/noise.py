
from pydub import AudioSegment
import noisereduce as nr
import numpy as np
import sys
print(sys.argv[1])

# pydubでWAVファイルを読み込む
audio = AudioSegment.from_wav(r"separated\htdemucs\testdata\vocals.wav")

# pydubオブジェクトからnumpy配列に変換
samples = np.array(audio.get_array_of_samples())

# サンプリングレートの取得
sample_rate = audio.frame_rate

# noisereduceでノイズ除去
reduced_noise = nr.reduce_noise(y=samples,
                                sr=sample_rate,
                                prop_decrease=int(sys.argv[1])/10,    # ノイズ除去の強さ (0.0～1.0の範囲)
                                time_mask_smooth_ms=10  # 時間マスクのスムージング (値を小さくすると、ノイズ除去が柔らかくなる)
                                )

# ノイズ除去後のデータをAudioSegmentオブジェクトに戻す
# numpy配列をpydubの音声データに変換
reduced_audio = AudioSegment(
    reduced_noise.tobytes(),
    frame_rate=sample_rate,
    sample_width=audio.sample_width,
    channels=audio.channels
)

reduced_audio.export(f"reduced_noise_testdata{sys.argv[1]}.wav", format="wav")
