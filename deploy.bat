@echo off
REM SignSync Meet Deployment Script for Windows
REM This script automates the deployment process for both frontend and backend

echo 🚀 Starting SignSync Meet Deployment...

REM Check if Node.js is installed
where node >nul 2>nul
if %errorlevel% neq 0 (
    echo [ERROR] Node.js is not installed. Please install Node.js v16 or higher.
    pause
    exit /b 1
)

REM Check if npm is installed
where npm >nul 2>nul
if %errorlevel% neq 0 (
    echo [ERROR] npm is not installed. Please install npm.
    pause
    exit /b 1
)

REM Check if Python is installed
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed. Please install Python 3.8 or higher.
    pause
    exit /b 1
)

echo [INFO] All requirements are met!

REM Deploy frontend
echo [INFO] Deploying frontend...
cd frontend

echo [INFO] Installing frontend dependencies...
call npm install

echo [INFO] Building production version...
call npm run build

REM Check if Firebase CLI is installed
where firebase >nul 2>nul
if %errorlevel% neq 0 (
    echo [WARNING] Firebase CLI not found. Installing...
    call npm install -g firebase-tools
)

echo [INFO] Deploying to Firebase...
call firebase deploy --only hosting

cd ..
echo [SUCCESS] Frontend deployed successfully!

REM Deploy backend
echo [INFO] Deploying backend...
cd backend

REM Create virtual environment if it doesn't exist
if not exist "venv" (
    echo [INFO] Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo [INFO] Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo [INFO] Installing backend dependencies...
call pip install -r requirements.txt

REM Check if .env file exists
if not exist ".env" (
    echo [WARNING] .env file not found. Please create one from env.example
    echo [INFO] You can copy env.example to .env and update the values
)

echo [SUCCESS] Backend setup completed!
echo [INFO] To start the backend server, run:
echo   cd backend
echo   venv\Scripts\activate.bat
echo   python app.py

cd ..

REM Setup AI model
echo [INFO] Setting up AI model...
cd ai-model

REM Create models directory if it doesn't exist
if not exist "models" mkdir models

REM Check if training data exists
if not exist "data" (
    echo [WARNING] Training data directory not found.
    echo [INFO] To train the model, create a 'data' directory with ASL images organized by letter
    echo [INFO] Then run: python train_model.py
) else (
    echo [INFO] Training data found. You can train the model with: python train_model.py
)

echo [SUCCESS] AI model setup completed!
cd ..

echo.
echo [SUCCESS] 🎉 Deployment completed successfully!
echo.
echo Next steps:
echo 1. Configure Firebase in frontend/src/firebase.js
echo 2. Set up environment variables in backend/.env
echo 3. Train the AI model with your data
echo 4. Start the backend server
echo.
echo For more information, see README.md
echo.
pause
