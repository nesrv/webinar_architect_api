@echo off
echo [*] Создание виртуального окружения Python 3.10 для SOAP примера...

REM Проверяем наличие Python 3.10
py -3.10 --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [!] Python 3.10 не найден. Установите Python 3.10 с python.org
    echo [!] Или используйте: winget install Python.Python.3.10
    pause
    exit /b 1
)

REM Создаем виртуальное окружение
py -3.10 -m venv venv310

REM Активируем окружение
call venv310\Scripts\activate.bat

REM Обновляем pip
python -m pip install --upgrade pip

REM Устанавливаем зависимости
pip install -r req.txt

echo [*] Виртуальное окружение Python 3.10 создано!
echo [*] Для активации: venv310\Scripts\activate.bat
pause