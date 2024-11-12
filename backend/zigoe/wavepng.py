import matplotlib.axes
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
from pydub import AudioSegment
import pyworld as pw
import sys
import crepe
import pyin
import os
if len(sys.argv)<=1:
    print("引数出せ")
    exit()
import time

def time_decorator(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()  # 開始時刻を記録
        result = func(*args, **kwargs)  # 関数を実行
        end_time = time.time()  # 終了時刻を記録
        elapsed_time = end_time - start_time  # 経過時間を計算
        print(f"Function {func.__name__} took {elapsed_time:.4f} seconds to execute.")
        return result
    return wrapper


audio = AudioSegment.from_wav(os.path.abspath(sys.argv[1]))  # ファイル名を変更してください

def sound(audio:AudioSegment,axs:matplotlib.axes._axes.Axes):
    # チャンネル数、サンプル幅、サンプルレートの取得
    channels = audio.channels
    sample_width = audio.sample_width
    sample_rate = audio.frame_rate
    # 音声データをnumpy配列に変換
    samples = np.array(audio.get_array_of_samples())
    # ステレオの場合、左チャンネルと右チャンネルに分割
    if channels == 2:
        samples = samples.reshape((-1, 2))
    # 波形を表示
    if channels == 2:
        axs.plot(samples[:, 0], label="Left Channel")
        axs.plot(samples[:, 1], label="Right Channel", alpha=0.7)
        axs.legend()
    else:
        axs.plot(samples, label="Mono Channel")
@time_decorator
def pwpitch1(audio:AudioSegment,axs:matplotlib.axes._axes.Axes):# ピッチ推定の設定
    frame_period = 5.0  # フレーム間隔 (ms)
    x=np.array(audio.get_array_of_samples())
    if len(x.shape) == 2:
        x = x.mean(axis=1)  # ステレオをモノラルに変換
    x = x / np.max(np.abs(x))
    fs=audio.frame_rate
    
    _f0, t = pw.dio(x, fs) 
    f0 = pw.stonemask(x, _f0, t, fs)
    axs.plot(t,f0,  label="M2o Channel")
@time_decorator
def pwpitch2(audio:AudioSegment,axs:matplotlib.axes._axes.Axes):# ピッチ推定の設定
    frame_period = 5.0  # フレーム間隔 (ms)
    x=np.array(audio.get_array_of_samples())
    if len(x.shape) == 2:
        x = x.mean(axis=1)  # ステレオをモノラルに変換
    x = x / np.max(np.abs(x))
    fs=audio.frame_rate
    f0, t = pw.harvest(x, fs)
    axs.plot(t,f0,  label="M2 Channel")
@time_decorator
def pyinpitch(audio:AudioSegment,axs:matplotlib.axes._axes.Axes):
    sr = audio.frame_rate
    x=np.array(audio.get_array_of_samples())
    pitch = pyin.estimate_pitch(x, sr)
    axs.plot(pitch,  label="pyin Channel")
@time_decorator
def crepitch(audio:AudioSegment,axs:matplotlib.axes._axes.Axes):
    x=np.array(audio.get_array_of_samples())
    time, frequency, confidence, activation = crepe.predict(x, audio.frame_rate, viterbi=True)# ピッチのプロット
    axs.plot(time, frequency, label='Pitch', color='blue')

    # 信頼度に基づいて色付け
    axs.scatter(time, frequency, c=confidence, cmap='viridis', alpha=0.5)


fig, axs = plt.subplots(2, 2, figsize=(10, 8))
#sound(audio,axs[0,0])
print("------------------------------------------")
pwpitch1(audio,axs[0,1])
print("------------------------------------------")
pwpitch2(audio,axs[1,0])
print("------------------------------------------")
crepitch(audio,axs[1,1])
print("------------------------------------------")
plt.title("Waveform of the Audio")
plt.xlabel("Sample Index")
plt.ylabel("Amplitude")
plt.show()