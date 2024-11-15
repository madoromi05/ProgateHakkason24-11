import numpy as np
from scipy.ndimage import gaussian_filter1d

def min_max_pitch(audio):
    pitch_data = audio[audio != 0]
    pitch_data=pitch_data[30:]
    smoothed_pitch = gaussian_filter1d(pitch_data, sigma=25,truncate=1000)
    mean = np.mean(smoothed_pitch)
    std_dev = np.std(smoothed_pitch)
    filtered_pitch = smoothed_pitch[(smoothed_pitch > mean - 2 * std_dev) & (smoothed_pitch < mean + 2 * std_dev)]
    return filtered_pitch
def min_max_pitch0(audio):
    return audio[audio != 0]
def min_max_pitch1(audio):
    audio = audio[audio != 0]
    return gaussian_filter1d(audio, sigma=1)


def min_max_pitch2(audio):
    audio = audio[audio != 0]
    return gaussian_filter1d(audio, sigma=30)
def min_max_pitch3(audio):
    audio = audio[audio != 0]
    return gaussian_filter1d(audio, sigma=1,truncate=1000)

def min_max_pitch4(audio):
    audio = audio[audio != 0]
    return gaussian_filter1d(audio, sigma=30,truncate=1000)







if __name__=="__main__":
    from func import loadwav
    import sys,os
    if len(sys.argv)<=1:
        print("引数出せ")
        filepath=r"C:\TK\github\hakkason3\backend\zigoe\moto\752912460.518347.wav"
    else:
        filepath=os.path.abspath(sys.argv[1])
    min_max_pitch(loadwav(filepath))