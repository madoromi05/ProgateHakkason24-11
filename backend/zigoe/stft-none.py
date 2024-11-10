
import numpy as np
import sys
import pyworld as pw
import scipy.io.wavfile as wav
import matplotlib.pyplot as plt
print(int(sys.argv[1])/10)
# 音声ファイルを読み込み
fs, x = wav.read(f"reduced_noise_testdata{sys.argv[1]}.wav")

if len(x.shape) == 2:
    x = x.mean(axis=1)  # ステレオをモノラルに変換

# 音声データを-1から1の範囲に正規化
x = x / np.max(np.abs(x))


# ピッチ推定の設定
frame_period = 5.0  # フレーム間隔 (ms)
# pyworldでピッチを推定
f0, time_axis = pw.harvest(x, fs, frame_period=frame_period,f0_floor=71.0, f0_ceil=800.0)
# ピッチの補完（途切れを補う）
f0 = pw.stonemask(x, f0, time_axis, fs)
# ピッチのプロット
print(f"F0 shape: {f0.shape}")
print(f0)
print(f"Temporal positions shape: {time_axis.shape}")
print(time_axis)
plt.plot(time_axis, f0)
plt.xlabel('Time [s]')
plt.ylabel('Pitch [Hz]')
plt.savefig(f'graph{sys.argv[1]}.png', format='png')
plt.show()
