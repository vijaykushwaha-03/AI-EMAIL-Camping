# Check prerequisites
Write-Host "Checking prerequisites..." -ForegroundColor Cyan

if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Error "Python is not installed. Please install Python 3.11+"
    exit 1
}

if (-not (Get-Command node -ErrorAction SilentlyContinue)) {
    Write-Error "Node.js is not installed. Please install Node.js 18+"
    exit 1
}

# Backend Setup
Write-Host "`nSetting up Backend..." -ForegroundColor Cyan
$backendDir = ".\backend"

if (-not (Test-Path "$backendDir\venv")) {
    Write-Host "Creating virtual environment..."
    python -m venv "$backendDir\venv"
}

# Activate venv and install requirements
Write-Host "Installing backend requirements..."
# We use a script block to run inside the venv context for setup
& "$backendDir\venv\Scripts\python.exe" -m pip install -r "$backendDir\requirements.txt"

# Run migrations
Write-Host "Running migrations..."
& "$backendDir\venv\Scripts\python.exe" "$backendDir\manage.py" migrate

# Frontend Setup
Write-Host "`nSetting up Frontend..." -ForegroundColor Cyan
$frontendDir = ".\frontend"

if (-not (Test-Path "$frontendDir\node_modules")) {
    Write-Host "Installing frontend dependencies..."
    Push-Location $frontendDir
    npm install
    Pop-Location
}

# Start Services
Write-Host "`nStarting Services..." -ForegroundColor Green

# Start Backend in a new window
Write-Host "Starting Backend Server..."
Start-Process powershell -ArgumentList "-NoExit", "-Command", "& '$PWD\$backendDir\venv\Scripts\python.exe' '$PWD\$backendDir\manage.py' runserver 0.0.0.0:8000"

# Start Frontend in a new window
Write-Host "Starting Frontend Server..."
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PWD\$frontendDir'; npm run dev"

Write-Host "`nApp is starting!" -ForegroundColor Green
Write-Host "Backend: http://localhost:8000/admin"
Write-Host "Frontend: http://localhost:5173"
