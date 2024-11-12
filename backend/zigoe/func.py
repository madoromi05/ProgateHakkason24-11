
import numpy as np
FRAMERATE=44100
def time_decorator(func):
    import time
    def wrapper(*args, **kwargs):
        start_time = time.time()  # 開始時刻を記録
        result = func(*args, **kwargs)  # 関数を実行
        end_time = time.time()  # 終了時刻を記録
        elapsed_time = end_time - start_time  # 経過時間を計算
        print(f"Function {func.__name__} took {elapsed_time:.4f} seconds to execute.")
        return result
    return wrapper


def is_iterable(x):
    from collections.abc import Iterable
    return isinstance(x, Iterable) and not isinstance(x, (str, bytes))

def auto_import(modules):
    import importlib
    for module,asname,where in modules:
        if asname:
            module_name=asname
        else:
            module_name=module
        if module_name not in globals():
            try:
                if where:
                    importwhere = importlib.import_module(where)
                    globals()[module_name] =  getattr(importwhere,where)
                else:
                    globals()[module_name] = importlib.import_module(module_name)
            except ImportError:
                print(f"モジュール '{module_name}' をインポートできませんでした。")


def formatingnumpy(data,yoko=True):
    if data.ndim == 2 and data.shape[1] == 2:
        return data if not yoko else data.T
    elif data.ndim == 2 and data.shape[0] == 2:
        return data if yoko else data.T
    else:
        print("不正な音声データです")
        return data

def writerwav(data,file="output.wav"):
    from scipy.io.wavfile import write
    if data.ndim == 1:
        data=np.clip(data, -1.0, 1.0)
        #data = (data * 65534).astype(np.uint16)
        print("モノラル音声です")
        write(file, FRAMERATE, data)
    elif data.ndim == 2 :
        data=formatingnumpy(data,yoko=False)
        print("ステレオ音声です")
        ndata=np.clip(data, -1.0, 1.0)
        write(file,FRAMERATE, ndata)
    else:
        print("不正な音声データです")
def writerpng(data,file="output.wav"):
    import matplotlib.pyplot as plt
    if data.ndim == 2 :
        data=formatingnumpy(data,yoko=True)[0]
    fig, ax = plt.subplots()
    ax.plot(data)
    ax.grid()
    fig.savefig(file)


def loadwav(file="input.wav"):
    import os
    from scipy.io.wavfile import read
    sample_rate, data = read(os.path.abspath(file))
    if data.dtype == np.int16:
        data = data / 32768.0  # 16ビットの範囲をfloat32にスケーリング
    elif data.dtype == np.int32:
        data = data / 2147483648.0  # 32ビットの範囲をfloat32にスケーリング
    elif data.dtype == np.uint8:
        data = (data - 128) / 128.0  # 8ビットの範囲をfloat32にスケーリング

    # 音声データの型をfloat32に変換
    data = data.astype(np.float32)
    FRAMERATE=sample_rate
    return data