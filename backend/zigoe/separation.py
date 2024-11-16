import numpy as np
import matplotlib.pyplot as plt
from func import writerwav,loadwav,formatingnumpy

def separation_demucs(audio):
    #インポート
    from demucs import pretrained
    from demucs.apply import apply_model
    import torch
    #データ整形
    if audio.ndim==2:
        audio=formatingnumpy(audio,yoko=True)
        audio_data = np.expand_dims(audio, axis=0) 
    elif audio.ndim==1:
        audio_data = np.stack([audio, audio], axis=0) 
        audio_data = np.expand_dims(audio_data, axis=0) 
    audio = audio_data.astype(np.float32)
    audio = audio / np.max(np.abs(audio))
    audio_tensor = torch.tensor(audio)
    #モデル生成
    model = pretrained.get_model("htdemucs")
    #実際に分離
    sources = apply_model(model, audio_tensor, device="cpu")
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