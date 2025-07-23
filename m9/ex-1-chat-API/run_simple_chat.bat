@echo off
echo Запуск простого чата без Redis...
uvicorn main_without_redis:app --reload --host 0.0.0.0 --port 8000
pause