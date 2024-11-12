import numpy as np
import matplotlib.pyplot as plt
from func import writerwav,loadwav,formatingnumpy
"""
このファイル内では関数の引数と返り値にモノラルのnumpy音声データ
"""
def separation_demucs(audio):
    from demucs import pretrained
    from demucs.apply import apply_model
    import torch

    audio_data = np.expand_dims(audio, axis=0) 
    audio_tensor = torch.tensor(audio_data)
    model = pretrained.get_model("htdemucs")


    sources = apply_model(model, audio_tensor, device="cpu")


    drums = sources[0, 0]
    bass = sources[0, 1]
    other = sources[0, 2]
    vocals = sources[0, 3]

    return vocals.numpy()
if __name__=="__main__":
    import librosa
    import sys,os

    if len(sys.argv)<=1:
        print("引数出せ")
        filepath=r"C:\TK\github\hakkason3\backend\zigoe\moto\752912460.518347.wav"
    else:
        filepath=os.path.abspath(sys.argv[1])
    audio_data=loadwav(filepath)
    y, sr = librosa.load(filepath, sr=44100,mono=False) 
    date=separation_demucs(y)
    writerwav(date)
    date=separation_demucs(formatingnumpy(audio_data,yoko=True))