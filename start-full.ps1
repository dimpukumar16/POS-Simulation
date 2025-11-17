# POS Simulator - Complete Startup Script
# This script starts both backend and frontend servers

Write-Host "=" * 70 -ForegroundColor Cyan
Write-Host "  🏪 POS SIMULATOR - COMPLETE SYSTEM STARTUP" -ForegroundColor Cyan
Write-Host "=" * 70 -ForegroundColor Cyan
Write-Host ""

$baseDir = "C:\Users\naikm\OneDrive\Desktop\pos_simulator"
$backendDir = Join-Path $baseDir "backend"
$frontendDir = Join-Path $baseDir "frontend"

# Function to check if port is in use
function Test-Port {
    param($Port)
    try {
        $listener = [System.Net.Sockets.TcpListener]::new([System.Net.IPAddress]::Loopback, $Port)
        $listener.Start()
        $listener.Stop()
        return $false  # Port is free
    } catch {
        return $true   # Port is in use
    }
}

# Check prerequisites
Write-Host "📋 Checking prerequisites..." -ForegroundColor Yellow
Write-Host ""

# Check Python
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✅ Python: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Python not found! Please install Python 3.11+" -ForegroundColor Red
    exit 1
}

# Check Node
try {
    $nodeVersion = node --version 2>&1
    Write-Host "✅ Node.js: $nodeVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Node.js not found! Please install Node.js 18+" -ForegroundColor Red
    exit 1
}

Write-Host ""

# Check if ports are available
if (Test-Port 5000) {
    Write-Host "⚠️  Port 5000 is already in use (Backend)" -ForegroundColor Yellow
    $kill = Read-Host "Kill existing process? (y/n)"
    if ($kill -eq 'y') {
        Stop-Process -Name python -Force -ErrorAction SilentlyContinue
        Write-Host "✅ Killed Python processes" -ForegroundColor Green
        Start-Sleep -Seconds 2
    }
}

if (Test-Port 5173) {
    Write-Host "⚠️  Port 5173 is already in use (Frontend)" -ForegroundColor Yellow
    $kill = Read-Host "Kill existing process? (y/n)"
    if ($kill -eq 'y') {
        Stop-Process -Name node -Force -ErrorAction SilentlyContinue
        Write-Host "✅ Killed Node processes" -ForegroundColor Green
        Start-Sleep -Seconds 2
    }
}

Write-Host ""
Write-Host "=" * 70 -ForegroundColor Cyan
Write-Host ""

# Start Backend
Write-Host "🔧 Starting Backend Server..." -ForegroundColor Yellow
Write-Host "Location: $backendDir" -ForegroundColor Gray
Write-Host ""

$backendJob = Start-Job -ScriptBlock {
    param($dir)
    Set-Location $dir
    python app.py
} -ArgumentList $backendDir

Write-Host "✅ Backend server starting..." -ForegroundColor Green
Write-Host "   URL: http://localhost:5000" -ForegroundColor Cyan
Start-Sleep -Seconds 3

Write-Host ""
Write-Host "=" * 70 -ForegroundColor Cyan
Write-Host ""

# Check if node_modules exists
if (-Not (Test-Path (Join-Path $frontendDir "node_modules"))) {
    Write-Host "📦 Node modules not found. Installing dependencies..." -ForegroundColor Yellow
    Write-Host ""
    
    Push-Location $frontendDir
    npm install
    Pop-Location
    
    Write-Host ""
    Write-Host "✅ Dependencies installed" -ForegroundColor Green
    Write-Host ""
}

# Start Frontend
Write-Host "🎨 Starting Frontend Server..." -ForegroundColor Yellow
Write-Host "Location: $frontendDir" -ForegroundColor Gray
Write-Host ""

$frontendJob = Start-Job -ScriptBlock {
    param($dir)
    Set-Location $dir
    npm run dev
} -ArgumentList $frontendDir

Write-Host "✅ Frontend server starting..." -ForegroundColor Green
Write-Host "   URL: http://localhost:5173" -ForegroundColor Cyan
Start-Sleep -Seconds 5

Write-Host ""
Write-Host "=" * 70 -ForegroundColor Cyan
Write-Host "  ✨ SYSTEM IS READY!" -ForegroundColor Green
Write-Host "=" * 70 -ForegroundColor Cyan
Write-Host ""
Write-Host "🌐 Open your browser and navigate to:" -ForegroundColor Yellow
Write-Host "   http://localhost:5173" -ForegroundColor Cyan
Write-Host ""
Write-Host "🔑 Default Login Credentials:" -ForegroundColor Yellow
Write-Host "   Admin:   admin / admin123" -ForegroundColor White
Write-Host "   Manager: manager / manager123" -ForegroundColor White
Write-Host "   Cashier: cashier / cashier123" -ForegroundColor White
Write-Host ""
Write-Host "📊 Backend API:" -ForegroundColor Yellow
Write-Host "   http://localhost:5000/api" -ForegroundColor Cyan
Write-Host ""
Write-Host "=" * 70 -ForegroundColor Cyan
Write-Host ""
Write-Host "💡 Tip: Use the Quick Login buttons on the login page!" -ForegroundColor Yellow
Write-Host ""
Write-Host "⚙️  Job IDs:" -ForegroundColor Gray
Write-Host "   Backend:  $($backendJob.Id)" -ForegroundColor Gray
Write-Host "   Frontend: $($frontendJob.Id)" -ForegroundColor Gray
Write-Host ""
Write-Host "=" * 70 -ForegroundColor Cyan
Write-Host ""
Write-Host "Press Ctrl+C to stop both servers, or close this window." -ForegroundColor Yellow
Write-Host "To view logs, open separate terminals and run:" -ForegroundColor Gray
Write-Host "  Backend:  cd $backendDir; python app.py" -ForegroundColor Gray
Write-Host "  Frontend: cd $frontendDir; npm run dev" -ForegroundColor Gray
Write-Host ""

# Keep script running and monitor jobs
try {
    while ($true) {
        Start-Sleep -Seconds 5
        
        # Check if jobs are still running
        $backendRunning = (Get-Job -Id $backendJob.Id).State -eq 'Running'
        $frontendRunning = (Get-Job -Id $frontendJob.Id).State -eq 'Running'
        
        if (-not $backendRunning) {
            Write-Host "❌ Backend server stopped!" -ForegroundColor Red
            break
        }
        if (-not $frontendRunning) {
            Write-Host "❌ Frontend server stopped!" -ForegroundColor Red
            break
        }
    }
} finally {
    Write-Host ""
    Write-Host "🛑 Stopping servers..." -ForegroundColor Yellow
    Stop-Job -Job $backendJob -ErrorAction SilentlyContinue
    Stop-Job -Job $frontendJob -ErrorAction SilentlyContinue
    Remove-Job -Job $backendJob -ErrorAction SilentlyContinue
    Remove-Job -Job $frontendJob -ErrorAction SilentlyContinue
    Write-Host "✅ Servers stopped." -ForegroundColor Green
}
