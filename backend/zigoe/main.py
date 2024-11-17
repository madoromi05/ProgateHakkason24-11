from separation import separation_demucs
from extraction import extraction_crepe,extraction_harvest,extraction_pyin,extraction_stonemask
from antiecho import echoproces,dummyproces
from pitch import min_max_pitch
from func import loadwav,writerpng
import numpy as np
import sys,os
import asyncio
def to_async(func):
    async def wrapper(*args, **kwargs):
        return await asyncio.to_thread(func, *args, **kwargs)
    return wrapper
@to_async
def separation_demucs_async(audio_data):return separation_demucs(audio_data)
@to_async
def dummyproces_async(audio_data):return dummyproces(audio_data)
@to_async
def extraction_harvest_async(audio_data):return extraction_harvest(audio_data)
@to_async
def min_max_pitch_async(audio_data):return min_max_pitch(audio_data)
async def path(path):
    audio_data=loadwav(path)
    audio_data = await separation_demucs_async(audio_data)
    audio_data = await dummyproces_async(audio_data)
    audio_data = await extraction_harvest_async(audio_data)
    audio_data = await min_max_pitch_async(audio_data)
    max_pitch = np.max(audio_data)
    min_pitch = np.min(audio_data)
    return {"max":max_pitch,"min":min_pitch}
async def main(audio_data):
    audio_data = await separation_demucs_async(audio_data)
    audio_data = await dummyproces_async(audio_data)
    audio_data = await extraction_harvest_async(audio_data)
    audio_data = await min_max_pitch_async(audio_data)
    max_pitch = np.max(audio_data)
    min_pitch = np.min(audio_data)
    return {"max":max_pitch,"min":min_pitch}


async def topng(audio_data,file="output.png"):
    writerpng(audio_data,file=file)
async def tosepartionpng(audio_data,file="output.png"):
    audio_data = await separation_demucs_async(audio_data)
    writerpng(audio_data,file=file)
    
async def topitchpng(audio_data,file="output.png"):
    audio_data = await separation_demucs_async(audio_data)
    audio_data = await dummyproces_async(audio_data)
    audio_data = await extraction_harvest_async(audio_data)
    writerpng(audio_data,file=file)

async def test():
    import random 
    path=random.choice([
        r"backend\zigoe\moto\752912460.876488.wav",
        r"backend\zigoe\moto\752912460.707662.wav",
        r"backend\zigoe\moto\752912460.518347.wav",])
    data=loadwav(file=path)
    return await main(data)


if __name__=="__main__":
    import sys,os
    if len(sys.argv)<=1:
        print("引数出せ")
        filepath=r"backend\zigoe\moto\752912460.518347.wav"
    else:
        filepath=os.path.abspath(sys.argv[1])
    main(loadwav(filepath))