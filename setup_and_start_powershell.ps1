# Parse arguments
param(
    [switch]$RunSetup
)

# Exit on errors
$ErrorActionPreference = "Stop"

# Terminal colors
$Green = "`e[32m"
$Yellow = "`e[33m"
$Red = "`e[31m"
$NoColor = "`e[0m"

# Check PowerShell version

if ($PSVersionTable.PSVersion.Major -lt 7) {
    Write-Host "${Red}PowerShell 7 or higher is required to run this script.${NoColor}"
    Write-Host "${Yellow}Please download and install PowerShell 7 from https://aka.ms/powershell${NoColor}"
    
    # Open the PowerShell 7 download page
    Start-Process "https://aka.ms/powershell"
    
    # Exit script
    exit 1
}

# Display help message
function Show-Help {
    Write-Host "${Yellow}Usage: script.ps1 [-RunSetup]${NoColor}"
    Write-Host "`nOptions:"
    Write-Host "  -RunSetup    Run the setup.py script (default: false)"
    Write-Host "`nExamples:"
    Write-Host "  ./script.ps1           # Start application without setup.py"
    Write-Host "  ./script.ps1 -RunSetup # Start application and run setup.py"
}



# Error handling function
function Handle-Error($Message) {
    Write-Host "${Red}Error: $Message${NoColor}"
    exit 1
}

# Install Certabo software (placeholder download link)
function Install-CertaboSoftware {
    Write-Host "${Yellow}Certabo software installation${NoColor}"
    Write-Host "1. Please download Certabo software from https://www.certabo.com/download-new/"
    Write-Host "2. Follow installation instructions, then press Enter to continue."
    Read-Host
}

# Check Docker installation
function Check-Docker {
    if (-not (Get-Command "docker" -ErrorAction SilentlyContinue)) {
        Handle-Error "Docker is not installed. Please install Docker and try again."
    }
}

# Ensure PostgreSQL container is running
function Ensure-PostgresContainer {
    if ((docker ps -aq -f "name=chess-postgres") -and (docker ps -aq -f "status=exited" -f "name=chess-postgres")) {
        Write-Host "${Yellow}Starting existing PostgreSQL container...${NoColor}"
        docker start chess-postgres
    }
    elseif (-not (docker ps -q -f "name=chess-postgres")) {
        Write-Host "${Yellow}Creating and starting new PostgreSQL container...${NoColor}"
        docker run --name chess-postgres -e POSTGRES_PASSWORD=mysecretpassword -p 5432:5432 -d postgres:14
    }
}

# Check if database and user exist
function Ensure-DatabaseAndUser {
    if (-not (docker exec chess-postgres psql -U postgres -tAc "SELECT 1 FROM pg_database WHERE datname='chessdb'" | Select-String "1")) {
        Write-Host "${Yellow}Creating database...${NoColor}"
        docker exec chess-postgres psql -U postgres -c "CREATE DATABASE chessdb;"
    }
    if (-not (docker exec chess-postgres psql -U postgres -tAc "SELECT 1 FROM pg_roles WHERE rolname='chessuser'" | Select-String "1")) {
        Write-Host "${Yellow}Creating user...${NoColor}"
        docker exec chess-postgres psql -U postgres -c "CREATE USER chessuser WITH PASSWORD 'chesspass';"
        docker exec chess-postgres psql -U postgres -c "GRANT ALL PRIVILEGES ON DATABASE chessdb TO chessuser;"
    }
}

# Setup backend environment
function Setup-Backend {
    Write-Host "${Yellow}Setting up backend...${NoColor}"
    Set-Location "backend"
    
    python -m venv venv
    .\venv\Scripts\Activate.ps1
    pip install --upgrade pip setuptools wheel
    pip install -r requirements.txt
    
    # Create database configuration
    Write-Output "[postgresql]`nhost = localhost`ndatabase = chessdb`nuser = chessuser`npassword = chesspass" | Set-Content "database/database.ini"
}

# Setup frontend
function Setup-Frontend {
    Write-Host "${Yellow}Setting up frontend...${NoColor}"
    Set-Location "..\frontend"
    npm install
}

# Run the script
try {
    Show-Help
    Install-CertaboSoftware
    Check-Docker
    Ensure-PostgresContainer
    Start-Sleep -Seconds 10 # Wait for PostgreSQL readiness
    Ensure-DatabaseAndUser
    Setup-Backend
    Setup-Frontend

    # Optional setup.py execution
    if ($RunSetup) {
        Write-Host "${Yellow}Running setup.py...${NoColor}"
        python setup.py
    }

    Write-Host "${Green}Setup complete and application started!${NoColor}"
}
catch {
    Handle-Error $_.Exception.Message
}
