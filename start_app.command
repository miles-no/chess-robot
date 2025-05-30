#!/bin/bash

echo "Starting the application..."
DIR="$(dirname "$0")"

# Open a new Terminal window and start the backend server
osascript -e 'tell app "Terminal" to do script "cd '"$DIR"'/backend && source venv/bin/activate && python server.py"'

# Open a new Terminal window and start the frontend application
osascript -e 'tell app "Terminal" to do script "cd '"$DIR"'/frontend && npm run dev"'
