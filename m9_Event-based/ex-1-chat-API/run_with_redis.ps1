# Запуск Redis и чат-сервера
Write-Host "Запуск Redis и чат-сервера..." -ForegroundColor Cyan

# Проверяем, запущен ли Redis
Write-Host "Проверка Redis..." -ForegroundColor Yellow
$redisRunning = $false

try {
    $result = redis-cli ping
    if ($result -eq "PONG") {
        $redisRunning = $true
        Write-Host "Redis уже запущен." -ForegroundColor Green
    }
} catch {
    $redisRunning = $false
}

if (-not $redisRunning) {
    Write-Host "Redis не запущен. Запускаем Redis..." -ForegroundColor Yellow
    Start-Process redis-server
    # Даем Redis время на запуск
    Start-Sleep -Seconds 2
}

# Запускаем чат-сервер
Write-Host "Запуск чат-сервера..." -ForegroundColor Cyan
uvicorn main:app --reload --host 0.0.0.0 --port 8000