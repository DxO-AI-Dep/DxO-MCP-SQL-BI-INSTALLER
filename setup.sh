#!/bin/bash

# Exit immediately if a command exits with a non-zero status.
set -e

PYTHON_CMD="python3" # Change this if your python command is different (e.g., "python")
VENV_DIR=".venv"

echo "--- Starting Setup Script ---"

# --- Argument Parsing ---
if [ -z "$1" ]; then
  echo "Error: Missing Google Drive URL argument."
  echo "Usage: ./setup.sh <your_google_drive_shareable_link>"
  exit 1
fi
GOOGLE_DRIVE_URL=$1
# --- End Argument Parsing ---

# Check if Python command exists
if ! command -v $PYTHON_CMD &> /dev/null
then
    echo "Error: $PYTHON_CMD command not found. Please ensure Python 3 is installed and in your PATH."
    exit 1
fi

echo "[1/4] Checking/Creating Python virtual environment ($VENV_DIR)..."
if [ ! -d "$VENV_DIR" ]; then
    $PYTHON_CMD -m venv $VENV_DIR
    echo "Virtual environment created."
else
    echo "Virtual environment already exists."
fi

# Activate virtual environment (syntax varies slightly between shells, this covers bash/zsh)
# Use source directly as the script runs in its own subshell
echo "[2/4] Activating virtual environment..."
source $VENV_DIR/bin/activate
echo "Virtual environment activated."

# Check for requirements.txt
if [ ! -f "requirements.txt" ]; then
    echo "Error: requirements.txt not found. Cannot install dependencies."
    # Deactivate venv just in case, although script exits
    deactivate || true 
    exit 1
fi

# Install dependencies
echo "[3/4] Installing Python dependencies from requirements.txt..."
pip install --upgrade pip # Ensure pip is up-to-date within the venv
pip install -r requirements.txt
echo "Dependencies installed."

# Check for download script
if [ ! -f "download_db.py" ]; then
    echo "Error: download_db.py not found. Cannot download database."
    deactivate || true
    exit 1
fi

# Run the download script
echo "[4/4] Running the database download and config generation script..."
# Pass the URL as an argument to the download script
python download_db.py "$GOOGLE_DRIVE_URL"

# Deactivation is generally not needed as the script exits, but good practice
# deactivate || true 

echo "--- Setup Script Finished ---" 