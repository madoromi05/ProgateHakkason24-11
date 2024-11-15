
import numpy as np
from func import FRAMERATE
from func import formatingnumpy
def extraction_stonemask(audio):# ピッチ推定の設定
    import pyworld as pw
    if len(audio.shape) == 2:
        audio = audio.mean(axis=1)  # ステレオをモノラルに変換
    audio = audio.astype(np.float64)
    audio = audio / np.max(np.abs(audio))
    
    _f0, t = pw.dio(audio, FRAMERATE) 
    f0 = pw.stonemask(audio, _f0, t, FRAMERATE)
    return f0
def extraction_harvest(audio):# ピッチ推定の設定
    
    import pyworld as pw
    print("bb1")
    if audio.ndim == 2:
        audio=formatingnumpy(audio,yoko=True)
        audio = np.mean(audio, axis=0)
    audio = audio.astype(np.float64)
    audio = audio / np.max(np.abs(audio))
    print("bb2")
    f0, t = pw.harvest(audio, FRAMERATE)
    print("bb3")
    return f0
def extraction_pyin(audio):
    import pyin
    return pyin.estimate_pitch(audio, FRAMERATE)

def extraction_crepe(audio):
    import crepe
    audio=formatingnumpy(audio,yoko=True)
    if audio.ndim == 2:
        audio = np.mean(audio, axis=0)
    time, frequency, confidence, activation = crepe.predict(audio,FRAMERATE, viterbi=True)
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
