# Quick Run Script - POS Simulator
# Simply runs both servers (assumes setup is complete)

Write-Host "============================================" -ForegroundColor Cyan
Write-Host "   POS Simulator - Quick Run" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

# Check if backend is already running
$backendRunning = Get-NetTCPConnection -LocalPort 5000 -ErrorAction SilentlyContinue
if ($backendRunning) {
    Write-Host "⚠️  Backend already running on port 5000" -ForegroundColor Yellow
} else {
    Write-Host "🚀 Starting Backend Server..." -ForegroundColor Green
    Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PSScriptRoot\backend'; Write-Host '=== Backend Server ===' -ForegroundColor Cyan; Write-Host 'Running on: http://localhost:5000/api' -ForegroundColor Green; Write-Host ''; python app.py"
    Start-Sleep -Seconds 3
}

# Check if frontend is already running
$frontendRunning = Get-NetTCPConnection -LocalPort 5173 -ErrorAction SilentlyContinue
if ($frontendRunning) {
    Write-Host "⚠️  Frontend already running on port 5173" -ForegroundColor Yellow
} else {
    Write-Host "🎨 Starting Frontend Server..." -ForegroundColor Green
    Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PSScriptRoot\frontend'; Write-Host '=== Frontend Server ===' -ForegroundColor Cyan; Write-Host 'Running on: http://localhost:5173' -ForegroundColor Green; Write-Host ''; npm run dev"
    Start-Sleep -Seconds 3
}

Write-Host ""
Write-Host "============================================" -ForegroundColor Cyan
Write-Host "✅ Servers Starting!" -ForegroundColor Green
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "📍 Access Points:" -ForegroundColor Yellow
Write-Host "   Frontend:  http://localhost:5173" -ForegroundColor White
Write-Host "   Backend:   http://localhost:5000/api" -ForegroundColor White
Write-Host ""
Write-Host "👤 Test Credentials:" -ForegroundColor Yellow
Write-Host "   Admin:    admin    / admin123" -ForegroundColor Cyan
Write-Host "   Manager:  manager  / manager123" -ForegroundColor Cyan
Write-Host "   Cashier:  cashier  / cashier123" -ForegroundColor Cyan
Write-Host ""
Write-Host "⏳ Waiting for servers to fully start..." -ForegroundColor Gray
Start-Sleep -Seconds 4

# Open browser
Write-Host "🌐 Opening browser..." -ForegroundColor Green
Start-Process "http://localhost:5173"

Write-Host ""
Write-Host "✨ Done! Check the new terminal windows." -ForegroundColor Green
Write-Host ""
Write-Host "💡 Tips:" -ForegroundColor Yellow
Write-Host "   - Press Ctrl+C in each terminal to stop servers" -ForegroundColor Gray
Write-Host "   - Check backend terminal for API logs" -ForegroundColor Gray
Write-Host "   - Check frontend terminal for build info" -ForegroundColor Gray
Write-Host ""
