from separation import separation_demucs
from extraction import extraction_crepe,extraction_harvest,extraction_pyin,extraction_stonemask
from antiecho import echoproces,dummyproces
from pitch import *
from func import loadwav,writerpng
import sys,os
def main(audio_data):
    audio_data=separation_demucs(audio_data)
    print("aa1")
    writerpng(audio_data,file="bunri1.png")
    print("aa2")
    audio_data=dummyproces(audio_data)
    print("aa3")
    data=extraction_harvest(audio_data)
    writerpng(data,file="bunri3.png")
    audio_data=min_max_pitch(data)
    writerpng(audio_data,file="bunri3mm.png")
    max_pitch = np.max(audio_data)
    min_pitch = np.min(audio_data)

    print(f"最高音の高さ: {max_pitch}")
    print(f"最低音の高さ: {min_pitch}")







if __name__=="__main__":
    import sys,os
    if len(sys.argv)<=1:
        print("引数出せ")
        filepath=r"C:\TK\github\hakkason3\backend\zigoe\moto\752912460.518347.wav"
    else:
        filepath=os.path.abspath(sys.argv[1])
    main(loadwav(filepath))