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
from func import FRAMERATE
def pwpitch1(audio):# ピッチ推定の設定
    
    if len(audio.shape) == 2:
        audio = audio.mean(axis=1)  # ステレオをモノラルに変換
    audio = audio / np.max(np.abs(audio))
    
    _f0, t = pw.dio(audio, FRAMERATE) 
    f0 = pw.stonemask(audio, _f0, t, FRAMERATE)
    return f0
def pwpitch2(audio):# ピッチ推定の設定
    if len(audio.shape) == 2:
        x = audio.mean(axis=1)  # ステレオをモノラルに変換
    audio = audio / np.max(np.abs(audio))
    f0, t = pw.harvest(audio, FRAMERATE)
    return f0
def pyinpitch(audio):
    return pyin.estimate_pitch(audio, FRAMERATE)

def crepitch(audio):
    time, frequency, confidence, activation = crepe.predict(audio, audio.frame_rate, viterbi=True)
    return frequency
