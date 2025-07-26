@echo off
echo Запуск чата без Redis...
set PYTHONPATH=%PYTHONPATH%;.
uvicorn main:app --reload --host 0.0.0.0 --port 8000
pause