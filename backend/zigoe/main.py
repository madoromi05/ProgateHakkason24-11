from separation import separation_demucs
from extraction import extraction_crepe,extraction_harvest,extraction_pyin,extraction_stonemask
from antiecho import echoproces,dummyproces
from pitch import min_max_pitch
from func import loadwav
import sys,os
def main(audio_data):
    audio_data=separation_demucs(audio_data)
    audio_data=dummyproces(audio_data)
    audio_data=extraction_harvest(audio_data)
    return min_max_pitch(audio_data)







if __name__=="__main__":
    if(sys.argv>1):
        main(loadwav(os.path.abspath(sys.argv[1])))
    else:
        print("引数をくれ")