
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
    from func import loadwav
    import sys,os
    if(sys.argv>1):
        extraction_harvest(loadwav(os.path.abspath(sys.argv[1])))
    else:
        print("引数をくれ")