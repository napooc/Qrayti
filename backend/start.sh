#!/bin/bash

echo ""
echo "================================"
echo "  Starting Qrayti Backend"
echo "================================"
echo ""

# Check if .env file exists
if [ ! -f .env ]; then
    echo "WARNING: .env file not found!"
    echo "Please run: python setup.py"
    echo ""
    exit 1
fi

# Start the server
echo "Starting server at http://localhost:8000"
echo "Press CTRL+C to stop"
echo ""
python main.py

