from separation import separation_demucs
from extraction import extraction_crepe,extraction_harvest,extraction_pyin,extraction_stonemask
from antiecho import echoproces,dummyproces
from pitch import min_max_pitch
from func import loadwav,writerpng
import sys,os
def main(audio_data):
    audio_data=separation_demucs(audio_data)
    print("aa1")
    writerpng(audio_data,file="bunri1.png")
    print("aa2")
    audio_data=dummyproces(audio_data)
    print("aa3")
    audio_data=extraction_harvest(audio_data)
    print("aa4")
    writerpng(audio_data,file="bunri2.png")
    return min_max_pitch(audio_data)







if __name__=="__main__":
    import sys,os
    if len(sys.argv)<=1:
        print("引数出せ")
        filepath=r"C:\TK\github\hakkason3\backend\zigoe\moto\752912460.518347.wav"
    else:
        filepath=os.path.abspath(sys.argv[1])
    main(loadwav(filepath))