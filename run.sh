#!/bin/bash
# Helper script to run the Raspberry Pi Object Recognition Application

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Error: Virtual environment not found!"
    echo "Please run ./setup.sh first"
    exit 1
fi

# Activate virtual environment and run the application
echo "Starting Raspberry Pi Object Recognition Application..."
source venv/bin/activate
python main.py
deactivate
