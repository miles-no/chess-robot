#!/bin/bash

# Exit immediately if a command exits with a non-zero status.
set -e

# Setup and start script for Miles Chess Robot

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
MAGENTA='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Function to display help message
display_help() {
    echo -e "${BLUE}🤖 Miles Chess Robot Setup and Start Script${NC}"
    echo
    echo -e "${CYAN}Usage: $0 [OPTIONS]${NC}"
    echo
    echo "This script sets up and starts the Miles Chess Robot application."
    echo
    echo -e "${YELLOW}Options:${NC}"
    echo -e "  ${GREEN}-h, --help     📚 Display this help message and exit${NC}"
    echo -e "  ${GREEN}--run-setup    🛠️  Run the setup.py script (default: false)${NC}"
    echo -e "  ${GREEN}--start        🚀 Start the application${NC}"
    echo
    echo -e "${YELLOW}Examples:${NC}"
    echo -e "  ${CYAN}$0 --start             🚀 Start the application without running setup.py${NC}"
    echo -e "  ${CYAN}$0 --start --run-setup 🚀🛠️  Start the application and run setup.py${NC}"
    echo
    echo -e "${MAGENTA}⚠️  Note: Make sure Docker is running before executing this script.${NC}"
}

# Default values
RUN_SETUP=false
START_APP=false

# Parse command line arguments
while [[ "$#" -gt 0 ]]; do
    case $1 in
        -h|--help)
            display_help
            exit 0
            ;;
        --run-setup)
            RUN_SETUP=true
            ;;
        --start)
            START_APP=true
            ;;
        *)
            echo -e "${RED}❌ Unknown parameter passed: $1${NC}"
            echo -e "Use '${CYAN}$0 --help${NC}' for usage information."
            exit 1
            ;;
    esac
    shift
done

# If no arguments provided or only --run-setup provided without --start, show help
if [ "$START_APP" = false ]; then
    display_help
    exit 0
fi

echo -e "${GREEN}🤖 Setting up Miles Chess Robot...${NC}"

# Function to handle errors
handle_error() {
    echo -e "${RED}❌ Error: $1${NC}"
    exit 1
}

# Check for Homebrew and install if missing
if ! command -v brew &> /dev/null; then
    echo -e "${YELLOW}Homebrew not found. Installing Homebrew...${NC}"
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)" || handle_error "Failed to install Homebrew"
else
    echo -e "${GREEN}Homebrew is installed.${NC}"
fi

# Check for Python and install if missing
if ! command -v python3 &> /dev/null; then
    echo -e "${YELLOW}Python 3 not found. Installing Python 3...${NC}"
    brew install python@3.11 || handle_error "Failed to install Python 3"
else
    echo -e "${GREEN}Python 3 is installed.${NC}"
fi

# Check for nvm and install if missing
if ! command -v nvm &> /dev/null; then
    echo -e "${YELLOW}nvm not found. Installing nvm...${NC}"
    curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.3/install.sh | bash || handle_error "Failed to install nvm"
    export NVM_DIR="$HOME/.nvm"
    [ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"  # This loads nvm
else
    echo -e "${GREEN}nvm is installed.${NC}"
fi

# Install and use the latest LTS version of Node.js
echo -e "${YELLOW}Installing and using the latest LTS version of Node.js...${NC}"
nvm install --lts || handle_error "Failed to install Node.js LTS"
nvm use --lts || handle_error "Failed to use Node.js LTS"

# Check if PostgreSQL container exists and start it if it's not running
echo -e "${YELLOW}Checking PostgreSQL container...${NC}"
if [ "$(docker ps -aq -f name=chess-postgres)" ]; then
    if [ "$(docker ps -aq -f status=exited -f name=chess-postgres)" ]; then
        echo -e "${YELLOW}Starting existing PostgreSQL container...${NC}"
        docker start chess-postgres || handle_error "Failed to start existing PostgreSQL container"
    else
        echo -e "${GREEN}PostgreSQL container is already running.${NC}"
    fi
else
    echo -e "${YELLOW}Creating and starting new PostgreSQL container...${NC}"
    docker run --name chess-postgres -e POSTGRES_PASSWORD=mysecretpassword -p 5432:5432 -d postgres:14 || handle_error "Failed to create and start new PostgreSQL container"
fi

# Wait for PostgreSQL to be ready
echo -e "${YELLOW}Waiting for PostgreSQL to be ready...${NC}"
sleep 10

# Check if database and user already exist
echo -e "${YELLOW}Checking database and user...${NC}"
if ! docker exec chess-postgres psql -U postgres -tAc "SELECT 1 FROM pg_database WHERE datname='chessdb'" | grep -q 1; then
    echo -e "${YELLOW}Creating database...${NC}"
    docker exec chess-postgres psql -U postgres -c "CREATE DATABASE chessdb;" || handle_error "Failed to create database"
else
    echo -e "${GREEN}Database 'chessdb' already exists.${NC}"
fi

if ! docker exec chess-postgres psql -U postgres -tAc "SELECT 1 FROM pg_roles WHERE rolname='chessuser'" | grep -q 1; then
    echo -e "${YELLOW}Creating user...${NC}"
    docker exec chess-postgres psql -U postgres -c "CREATE USER chessuser WITH PASSWORD 'chesspass';" || handle_error "Failed to create user"
    docker exec chess-postgres psql -U postgres -c "GRANT ALL PRIVILEGES ON DATABASE chessdb TO chessuser;" || handle_error "Failed to grant privileges"
else
    echo -e "${GREEN}User 'chessuser' already exists.${NC}"
fi

# Function to setup and start backend
setup_backend() {
    echo -e "${YELLOW}🔧 Setting up backend...${NC}"
    cd backend || handle_error "Failed to change directory to backend"
    python3 -m venv venv || handle_error "Failed to create virtual environment"
    source venv/bin/activate || handle_error "Failed to activate virtual environment"
    pip install --upgrade pip setuptools wheel || handle_error "Failed to install setuptools and wheel"
    pip install -r requirements.txt || handle_error "Failed to install requirements"
    
    if [ "$RUN_SETUP" = true ]; then
        echo -e "${CYAN}🛠️  Running setup.py...${NC}"
        DB_HOST=localhost DB_NAME=chessdb DB_USER=postgres DB_PASSWORD=mysecretpassword python setup.py || handle_error "Failed to run setup.py"
    else
        echo -e "${MAGENTA}⏩ Skipping setup.py (use --run-setup flag to run it)${NC}"
    fi
    
    echo -e "${GREEN}🚀 Starting backend server...${NC}"
    python server.py &
    cd ..
}

# Function to setup and start frontend
setup_frontend() {
    echo -e "${YELLOW}🔧 Setting up frontend...${NC}"
    cd frontend || handle_error "Failed to change directory to frontend"
    npm install || handle_error "Failed to install frontend dependencies"
    echo -e "${GREEN}🚀 Starting frontend...${NC}"
    npm run dev &
    cd ..
}

# Run backend and frontend setup in parallel
setup_backend &
setup_frontend &

# Wait for both processes to finish
wait

echo -e "${GREEN}✅ Setup complete and application started!${NC}"
