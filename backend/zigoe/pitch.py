def func(audio):
    #兵站か
def min_max_pitch(audio):
    pass






if __name__=="__main__":
    from func import loadwav
    import sys,os
    if len(sys.argv)<=1:
        print("引数出せ")
        filepath=r"C:\TK\github\hakkason3\backend\zigoe\moto\752912460.518347.wav"
    else:
        filepath=os.path.abspath(sys.argv[1])
    min_max_pitch(loadwav(filepath))