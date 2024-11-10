@echo off
if "%1"=="" (
    echo 仮想環境のパスを指定してください。
    exit /b
)

call zigoe\Scripts\activate.bat

python C:\path\to\your\script.py %1

deactivate
pause