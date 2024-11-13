@echo off
python -m venv myvenv
call myvenv\Scripts\activate.bat
python --version
echo 仮想環境起動
python.exe -m pip install --upgrade pip
if exist requirements.txt (
    echo ミッケ
    pip install -r requirements.txt
) else (
    echo requirements.txt が見つかりません。
)
deactivate
pause