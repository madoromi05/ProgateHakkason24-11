@echo off
for /L %%i in (1, 1, 10) do (
    echo %%i
    python noise.py %%i
    python stft-none.py %%i
)
pause