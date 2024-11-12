def min_max_pitch(audio):
    pass






if __name__=="__main__":
    from func import loadwav
    import sys,os
    if(sys.argv>1):
        min_max_pitch(loadwav(os.path.abspath(sys.argv[1])))
    else:
        print("引数をくれ")