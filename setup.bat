@echo off
setlocal

REM --- Configuration ---
set PYTHON_CMD=py -3
set VENV_DIR=.venv
REM --- End Configuration ---

echo --- Starting Setup Script ---

REM --- Argument Parsing ---
if "%~1"=="" (
    echo Error: Missing Google Drive URL argument.
    echo Usage: setup.bat ^<your_google_drive_shareable_link^>
    pause
    exit /b 1
)
set GOOGLE_DRIVE_URL=%~1
REM --- End Argument Parsing ---

REM Check if Python command exists
%PYTHON_CMD% --version > nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Python 3 command not found (tried "%PYTHON_CMD%"). Please ensure Python 3 is installed and in your PATH.
    echo You might need to install it from https://www.python.org/ or use 'python'/'python3' instead of 'py -3' in the script.
    pause
    exit /b 1
)

echo [1/4] Checking/Creating Python virtual environment (%VENV_DIR%)...
if not exist "%VENV_DIR%\Scripts\activate.bat" (
    echo Creating virtual environment...
    %PYTHON_CMD% -m venv %VENV_DIR%
    if %errorlevel% neq 0 (
        echo Error: Failed to create virtual environment.
        pause
        exit /b 1
    )
    echo Virtual environment created.
) else (
    echo Virtual environment already exists.
)

REM Activate virtual environment
echo [2/4] Activating virtual environment...
call "%VENV_DIR%\Scripts\activate.bat"
if %errorlevel% neq 0 (
    echo Error: Failed to activate virtual environment.
    pause
    exit /b 1
)
echo Virtual environment activated.

REM Check for requirements.txt
if not exist "requirements.txt" (
    echo Error: requirements.txt not found. Cannot install dependencies.
    call "%VENV_DIR%\Scripts\deactivate.bat" || echo Deactivation might fail if activation failed.
    pause
    exit /b 1
)

REM Install dependencies
echo [3/4] Installing Python dependencies from requirements.txt...
pip install --upgrade pip
if %errorlevel% neq 0 (
    echo Warning: Failed to upgrade pip. Continuing with installation...
)
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo Error: Failed to install dependencies from requirements.txt.
    call "%VENV_DIR%\Scripts\deactivate.bat" || echo Deactivation might fail if activation failed.
    pause
    exit /b 1
)
echo Dependencies installed.

REM Check for download script
if not exist "download_db.py" (
    echo Error: download_db.py not found. Cannot download database.
    call "%VENV_DIR%\Scripts\deactivate.bat" || echo Deactivation might fail if activation failed.
    pause
    exit /b 1
)

REM Run the download script
echo [4/4] Running the database download and config generation script...
REM Pass the URL as an argument to the download script
python download_db.py "%GOOGLE_DRIVE_URL%"
if %errorlevel% neq 0 (
    echo Error: The download_db.py script failed.
    call "%VENV_DIR%\Scripts\deactivate.bat" || echo Deactivation might fail if activation failed.
    pause
    exit /b 1
)

REM Deactivation happens implicitly when script exits or via endlocal

echo --- Setup Script Finished ---
endlocal
REM Add a pause at the end for successful execution only if needed for debugging
REM pause
exit /b 0 