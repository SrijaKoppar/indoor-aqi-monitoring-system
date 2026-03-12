@echo off
REM Air Quality Monitor - Development Startup Script (Windows)
REM This script starts both the React frontend and FastAPI backend

echo.
echo 🚀 Air Quality Monitor - Development Startup
echo ==============================================
echo.

REM Check if Node.js is installed
where node >nul 2>nul
if %errorlevel% neq 0 (
    echo ❌ Node.js is not installed
    echo    Please install Node.js from https://nodejs.org
    pause
    exit /b 1
)

REM Check if Python is installed
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo ❌ Python is not installed
    echo    Please install Python from https://www.python.org
    pause
    exit /b 1
)

for /f "tokens=*" %%i in ('node --version') do set NODE_VERSION=%%i
for /f "tokens=*" %%i in ('python --version') do set PYTHON_VERSION=%%i

echo ✓ Node.js version: %NODE_VERSION%
echo ✓ Python version: %PYTHON_VERSION%
echo.

REM Step 1: Setup Frontend
echo 📦 Setting up frontend...
if not exist "node_modules" (
    call pnpm install
) else (
    echo    ✓ Dependencies already installed
)

if not exist ".env.local" (
    echo    📝 Creating .env.local...
    copy .env.local.example .env.local
    echo    ✓ .env.local created
)

echo ✓ Frontend setup complete
echo.

REM Step 2: Setup Backend
echo 📦 Setting up backend...
cd backend

if not exist "venv" (
    echo    🐍 Creating Python virtual environment...
    python -m venv venv
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Install dependencies
pip show fastapi >nul 2>nul
if %errorlevel% neq 0 (
    echo    📥 Installing Python dependencies...
    pip install -r requirements.txt
) else (
    echo    ✓ Dependencies already installed
)

if not exist ".env" (
    echo    📝 Creating .env...
    copy .env.example .env
    echo    ✓ .env created
)

echo ✓ Backend setup complete
echo.

cd ..

REM Step 3: Display instructions
echo ========================================
echo ✅ Setup complete!
echo ========================================
echo.
echo To start development, open TWO terminals:
echo.
echo Terminal 1 - Frontend:
echo   ^> pnpm dev
echo   → http://localhost:3000
echo.
echo Terminal 2 - Backend:
echo   ^> cd backend
echo   ^> venv\Scripts\activate
echo   ^> uvicorn main:app --reload
echo   → http://localhost:8000
echo   → API Docs: http://localhost:8000/docs
echo.
echo ========================================
echo.
pause
