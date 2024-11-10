@echo off
python -m venv zigoe

call zigoe\Scripts\activate.bat
if exist requirements.txt (
    pip install -r requirements.txt
) else (
    echo requirements.txt が見つかりません。
)
deactivate
pause