@echo off
echo.
echo ================================
echo   Starting Qrayti Backend
echo ================================
echo.

REM Check if .env file exists
if not exist .env (
    echo WARNING: .env file not found!
    echo Please run: python setup.py
    echo.
    pause
    exit /b 1
)

REM Start the server
echo Starting server at http://localhost:8000
echo Press CTRL+C to stop
echo.
python main.py

