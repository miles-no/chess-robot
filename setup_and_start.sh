#!/bin/bash

# Exit immediately if a command exits with a non-zero status.
set -e

# Setup and start script for Miles Chess Robot

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Function to display help message
display_help() {
    echo "Usage: $0 [OPTIONS]"
    echo
    echo "This script sets up and starts the Miles Chess Robot application."
    echo
    echo "Options:"
    echo "  -h, --help     Display this help message and exit"
    echo "  --run-setup    Run the setup.py script (default: false)"
    echo
    echo "Examples:"
    echo "  $0                   # Start the application without running setup.py"
    echo "  $0 --run-setup       # Start the application and run setup.py"
    echo
    echo "Note: Make sure Docker is running before executing this script."
}

# Default value for running setup.py
RUN_SETUP=false

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
        *)
            echo -e "${RED}Unknown parameter passed: $1${NC}"
            echo "Use '$0 --help' for usage information."
            exit 1
            ;;
    esac
    shift
done

echo -e "${GREEN}Setting up Miles Chess Robot...${NC}"

# Function to handle errors
handle_error() {
    echo -e "${RED}Error: $1${NC}"
    exit 1
}

prompt_certabo_software_installation() {
    echo -e "${YELLOW}Certabo software installation${NC}"
    
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        SOFTWARE_URL="https://www.certabo.com/wp-content/uploads/SOFTWARE/Release/Mac/Certabo%20Chess%204.52_Nov_2023.zip"
    elif [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
        # Windows
        SOFTWARE_URL="https://www.certabo.com/download-new/"  # Update this with the correct Windows URL when available
    else
        echo -e "${RED}Unsupported operating system${NC}"
        return 1
    fi

    echo -e "${YELLOW}Please follow these steps to install the Certabo software:${NC}"
    echo -e "1. Download the Certabo software from: ${GREEN}$SOFTWARE_URL${NC}"
    echo -e "2. Once downloaded, open the file and follow the installation instructions."
    echo -e "3. After installation is complete, return to this terminal and press Enter to continue."

    read -p "Press Enter when you have completed the Certabo software installation..."

    echo -e "${GREEN}Thank you for installing the Certabo software. Continuing with the setup...${NC}"
}

# Install Certabo software
prompt_certabo_software_installation

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

# Setup backend
echo -e "${YELLOW}Setting up backend...${NC}"
cd backend || handle_error "Failed to change directory to backend"

# Create virtual environment
echo -e "${YELLOW}Creating virtual environment...${NC}"
python3 -m venv venv || handle_error "Failed to create virtual environment"

# Activate virtual environment
echo -e "${YELLOW}Activating virtual environment...${NC}"
source venv/bin/activate || handle_error "Failed to activate virtual environment"

# Install setuptools and wheel first
echo -e "${YELLOW}Installing setuptools and wheel...${NC}"
pip install --upgrade pip setuptools wheel || handle_error "Failed to install setuptools and wheel"

# Install requirements
echo -e "${YELLOW}Installing requirements...${NC}"
pip install -r requirements.txt || handle_error "Failed to install requirements"

# If NumPy installation fails, try to install it separately
if ! pip show numpy > /dev/null 2>&1; then
    echo -e "${YELLOW}NumPy installation failed. Trying to install latest version...${NC}"
    pip install numpy || handle_error "Failed to install NumPy"
fi

# Create database.ini
echo -e "${YELLOW}Creating database.ini...${NC}"
cat << EOF > database/database.ini || handle_error "Failed to create database.ini"
[postgresql]
host = localhost
database = chessdb
user = chessuser
password = chesspass
EOF

# Setup Stockfish
echo -e "${YELLOW}Setting up Stockfish...${NC}"
if ! command -v stockfish &> /dev/null; then
    echo -e "${YELLOW}Stockfish not found. Installing Stockfish...${NC}"
    brew install stockfish || handle_error "Failed to install Stockfish"
else
    echo -e "${GREEN}Stockfish is already installed.${NC}"
fi

# Get Stockfish path
STOCKFISH_PATH=$(which stockfish)
if [ -z "$STOCKFISH_PATH" ]; then
    handle_error "Stockfish path not found"
fi

# Create config.py with Stockfish path
echo -e "${YELLOW}Creating config.py with Stockfish path...${NC}"
cat << EOF > config.py || handle_error "Failed to create config.py"
STOCKFISH_PATH = "$STOCKFISH_PATH"
EOF

# Run setup.py only if the flag is set
if [ "$RUN_SETUP" = true ]; then
    echo -e "${YELLOW}Running setup.py...${NC}"
    DB_HOST=localhost DB_NAME=chessdb DB_USER=postgres DB_PASSWORD=mysecretpassword python setup.py || handle_error "Failed to run setup.py"
else
    echo -e "${YELLOW}Skipping setup.py (use --run-setup flag to run it)${NC}"
fi

# Start backend server in a new terminal window
echo -e "${YELLOW}Starting backend server in a new terminal...${NC}"
osascript -e 'tell app "Terminal" to do script "cd '"$(pwd)"' && source venv/bin/activate && python server.py"' || handle_error "Failed to start backend server"

# Setup frontend
echo -e "${YELLOW}Setting up frontend...${NC}"
cd ../frontend || handle_error "Failed to change directory to frontend"
npm install || handle_error "Failed to install frontend dependencies"

# Start frontend in a new terminal window
echo -e "${YELLOW}Starting frontend in a new terminal...${NC}"
osascript -e 'tell app "Terminal" to do script "cd '"$(pwd)"' && npm run dev"' || handle_error "Failed to start frontend"

echo -e "${GREEN}Setup complete and application started in separate terminals!${NC}"
