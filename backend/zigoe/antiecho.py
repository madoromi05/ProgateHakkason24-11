import numpy as np
from func import FRAMERATE


def echoproces(audio):
    import noisereduce as nr
    reduced_noise = nr.reduce_noise(y=audio,
                                    sr=FRAMERATE,
                                    prop_decrease=0.8,    # ノイズ除去の強さ (0.0～1.0の範囲)
                                    time_mask_smooth_ms=10  # 時間マスクのスムージング (値を小さくすると、ノイズ除去が柔らかくなる)
                                    )

    return reduced_noise
def dummyproces(audio):return audio

if __name__=="__main__":
    from func import loadwav
    import sys,os
    if(sys.argv>1):
        echoproces(loadwav(os.path.abspath(sys.argv[1])))
    else:
        print("引数をくれ")