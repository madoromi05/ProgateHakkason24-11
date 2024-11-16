@echo off
if "%1"=="" (
    echo 仮想環境でのパスを指定してください。
    exit /b
)

call myvenv\Scripts\activate.bat
echo 仮想環境起動

python C:\path\to\your\script.py %1

deactivate
pause