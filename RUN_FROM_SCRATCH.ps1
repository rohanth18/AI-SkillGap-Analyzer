# ============================================================================
# RUN PROJECT FROM SCRATCH - Windows PowerShell Script
# ============================================================================
# This script sets up and runs the AI SkillGap Analyzer project from scratch
# ============================================================================

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  AI SkillGap Analyzer - Setup & Run" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Get the project root directory
$projectRoot = $PSScriptRoot
if (-not $projectRoot) {
    $projectRoot = Get-Location
}

$backendPath = Join-Path $projectRoot "backend"
$frontendPath = Join-Path $projectRoot "frontend"

# ============================================================================
# STEP 1: BACKEND SETUP
# ============================================================================
Write-Host "[1/4] Setting up Backend..." -ForegroundColor Yellow

Set-Location $backendPath

# Check if venv exists, create if not
if (-not (Test-Path "venv\Scripts\python.exe")) {
    Write-Host "  Creating virtual environment..." -ForegroundColor Gray
    python -m venv venv
    if ($LASTEXITCODE -ne 0) {
        Write-Host "  ERROR: Failed to create virtual environment" -ForegroundColor Red
        Write-Host "  Make sure Python 3.9+ is installed and in PATH" -ForegroundColor Red
        exit 1
    }
}

# Install backend dependencies
Write-Host "  Installing Python packages..." -ForegroundColor Gray
.\venv\Scripts\python.exe -m pip install --upgrade pip --quiet
.\venv\Scripts\python.exe -m pip install -r requirements.txt --quiet

if ($LASTEXITCODE -ne 0) {
    Write-Host "  ERROR: Failed to install backend dependencies" -ForegroundColor Red
    exit 1
}

# Install spaCy model
Write-Host "  Installing spaCy language model..." -ForegroundColor Gray
if (Test-Path "en_core_web_sm-3.7.1-py3-none-any.whl") {
    .\venv\Scripts\python.exe -m pip install en_core_web_sm-3.7.1-py3-none-any.whl --quiet
} else {
    Write-Host "  Warning: spaCy model wheel not found, trying to download..." -ForegroundColor Yellow
    .\venv\Scripts\python.exe -m pip install https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-3.7.1/en_core_web_sm-3.7.1-py3-none-any.whl --quiet
}

Write-Host "  ✓ Backend setup complete" -ForegroundColor Green
Write-Host ""

# ============================================================================
# STEP 2: FRONTEND SETUP
# ============================================================================
Write-Host "[2/4] Setting up Frontend..." -ForegroundColor Yellow

Set-Location $frontendPath

# Check if node_modules exists
if (-not (Test-Path "node_modules")) {
    Write-Host "  Installing npm packages..." -ForegroundColor Gray
    npm install
    if ($LASTEXITCODE -ne 0) {
        Write-Host "  ERROR: Failed to install frontend dependencies" -ForegroundColor Red
        Write-Host "  Make sure Node.js 16+ is installed" -ForegroundColor Red
        exit 1
    }
} else {
    Write-Host "  Frontend dependencies already installed" -ForegroundColor Gray
}

Write-Host "  ✓ Frontend setup complete" -ForegroundColor Green
Write-Host ""

# ============================================================================
# STEP 3: START SERVERS
# ============================================================================
Write-Host "[3/4] Starting servers..." -ForegroundColor Yellow
Write-Host ""

# Start backend in new window
Write-Host "  Starting Backend Server (port 5000)..." -ForegroundColor Gray
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$backendPath'; Write-Host 'Backend Server Starting...' -ForegroundColor Cyan; .\venv\Scripts\python.exe app.py"

# Wait a moment for backend to start
Start-Sleep -Seconds 2

# Start frontend in new window
Write-Host "  Starting Frontend Server (port 5173)..." -ForegroundColor Gray
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$frontendPath'; Write-Host 'Frontend Server Starting...' -ForegroundColor Cyan; npm run dev"

Write-Host "  ✓ Servers starting in separate windows" -ForegroundColor Green
Write-Host ""

# ============================================================================
# STEP 4: WAIT AND VERIFY
# ============================================================================
Write-Host "[4/4] Verifying servers..." -ForegroundColor Yellow
Write-Host "  Waiting for servers to start..." -ForegroundColor Gray
Start-Sleep -Seconds 8

$backendRunning = $false
$frontendRunning = $false

# Check if ports are listening
$ports = Get-NetTCPConnection -LocalPort 5000,5173 -ErrorAction SilentlyContinue
if ($ports) {
    foreach ($port in $ports) {
        if ($port.LocalPort -eq 5000) { $backendRunning = $true }
        if ($port.LocalPort -eq 5173) { $frontendRunning = $true }
    }
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  STATUS" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
if ($backendRunning) {
    Write-Host "  ✓ Backend:  http://127.0.0.1:5000" -ForegroundColor Green
} else {
    Write-Host "  ✗ Backend:  Not detected (check the backend window)" -ForegroundColor Yellow
}
if ($frontendRunning) {
    Write-Host "  ✓ Frontend: http://localhost:5173" -ForegroundColor Green
} else {
    Write-Host "  ✗ Frontend: Not detected (check the frontend window)" -ForegroundColor Yellow
}
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  NEXT STEPS" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  1. Open your browser and go to: http://localhost:5173" -ForegroundColor White
Write-Host "  2. Click 'Register' to create your account" -ForegroundColor White
Write-Host "  3. First user automatically becomes ADMIN" -ForegroundColor White
Write-Host "  4. Login and start using the application!" -ForegroundColor White
Write-Host ""
Write-Host "  To stop servers: Press Ctrl+C in each window" -ForegroundColor Gray
Write-Host ""

