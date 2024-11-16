import sys,os
folder_path = os.path.join(os.path.dirname(__file__))
if folder_path not in sys.path:sys.path.append(folder_path)
print("zigoeのimport完了")
from main import main as zigoe_async
from main import topng as topng_async
from main import topitchpng as topitchpng_async
from main import tosepartionpng as tosepartionpng_async
from main import test as testdata_async