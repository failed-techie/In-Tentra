@echo off
REM ================================================================
REM INTENTRA - Multi-Agent AI Trading System
REM Setup Script for Windows
REM ================================================================

echo ================================================================
echo INTENTRA - Multi-Agent AI Trading System
echo Setup Script for Windows
echo ================================================================
echo.

REM Check if Python is installed
echo [1/6] Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.9 or higher from https://www.python.org
    echo Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)

for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo Found Python %PYTHON_VERSION%
echo.

REM Create virtual environment
echo [2/6] Creating virtual environment...
if exist venv (
    echo Virtual environment already exists. Skipping creation.
) else (
    python -m venv venv
    if errorlevel 1 (
        echo ERROR: Failed to create virtual environment
        pause
        exit /b 1
    )
    echo Virtual environment created successfully
)
echo.

REM Activate virtual environment
echo [3/6] Activating virtual environment...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo ERROR: Failed to activate virtual environment
    pause
    exit /b 1
)
echo Virtual environment activated
echo.

REM Upgrade pip
echo [4/6] Upgrading pip...
python -m pip install --upgrade pip setuptools wheel
if errorlevel 1 (
    echo WARNING: Failed to upgrade pip, continuing anyway...
)
echo.

REM Install requirements
echo [5/6] Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)
echo Dependencies installed successfully
echo.

REM Copy .env.example to .env
echo [6/6] Setting up environment file...
if exist .env (
    echo .env file already exists. Skipping copy.
    echo To reset, delete .env and run this script again.
) else (
    copy .env.example .env >nul
    echo .env file created from template
    echo.
    echo IMPORTANT: Edit .env and add your API keys!
)
echo.

REM Create logs directory
if not exist logs mkdir logs
echo Logs directory ready
echo.

REM Success message
echo ================================================================
echo Setup Complete!
echo ================================================================
echo.
echo Next steps:
echo   1. Edit .env and add your API keys:
echo      - GROQ_API_KEY (from https://console.groq.com)
echo      - ALPACA_API_KEY (from https://alpaca.markets)
echo      - ALPACA_SECRET_KEY
echo.
echo   2. Activate the virtual environment:
echo      venv\Scripts\activate
echo.
echo   3. Run the application:
echo      python main.py
echo.
echo   4. Access the API at http://localhost:8000
echo.
echo ================================================================
pause
