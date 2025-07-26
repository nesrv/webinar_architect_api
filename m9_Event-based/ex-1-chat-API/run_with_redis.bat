@echo off
echo Запуск Redis и чат-сервера...

:: Проверяем, запущен ли Redis
echo Проверка Redis...
redis-cli ping > nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Redis не запущен. Запускаем Redis...
    start "Redis Server" redis-server
    :: Даем Redis время на запуск
    timeout /t 2 > nul
) else (
    echo Redis уже запущен.
)

:: Запускаем чат-сервер
echo Запуск чат-сервера...
uvicorn main:app --reload --host 0.0.0.0 --port 8000