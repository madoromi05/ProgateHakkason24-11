import sys,os
folder_path = os.path.join(os.path.dirname(__file__))
if folder_path not in sys.path:sys.path.append(folder_path)
print("zigoeのimport完了")
from main import (
    main as zigoe_async,
    topng as topng_async,
    topitchpng as topitchpng_async,
    tosepartionpng as tosepartionpng_async,
    test as testdata_async,
    path as path_async,
)