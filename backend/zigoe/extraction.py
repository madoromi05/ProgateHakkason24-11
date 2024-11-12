
import numpy as np
from func import FRAMERATE
def extraction_stonemask(audio):# ピッチ推定の設定
    import pyworld as pw
    if len(audio.shape) == 2:
        audio = audio.mean(axis=1)  # ステレオをモノラルに変換
    audio = audio / np.max(np.abs(audio))
    
    _f0, t = pw.dio(audio, FRAMERATE) 
    f0 = pw.stonemask(audio, _f0, t, FRAMERATE)
    return f0
def extraction_harvest(audio):# ピッチ推定の設定
    import pyworld as pw
    if len(audio.shape) == 2:
        x = audio.mean(axis=1)  # ステレオをモノラルに変換
    audio = audio / np.max(np.abs(audio))
    f0, t = pw.harvest(audio, FRAMERATE)
    return f0
def extraction_pyin(audio):
    import pyin
    return pyin.estimate_pitch(audio, FRAMERATE)

def extraction_crepe(audio):
    import crepe
    time, frequency, confidence, activation = crepe.predict(audio, audio.frame_rate, viterbi=True)
    return frequency
if __name__=="__main__":
    from func import loadwav,writerwav
    import sys,os
    if len(sys.argv)<=1:
        print("引数出せ")
        filepath=r"C:\TK\github\hakkason3\backend\zigoe\moto\752912460.518347.wav"
    else:
        filepath=os.path.abspath(sys.argv[1])
    extraction_harvest(loadwav(filepath))
