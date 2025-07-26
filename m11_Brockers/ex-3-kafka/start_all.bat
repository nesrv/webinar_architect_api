@echo off
echo [*] Запуск всех компонентов системы Kafka...
echo [*] Откроются 3 окна терминала

start "Kafka Monitor" start_monitor.bat
timeout /t 2 /nobreak >nul

start "Kafka Consumer" start_consumer.bat
timeout /t 2 /nobreak >nul

start "Kafka Producer" start_producer.bat

echo [*] Все компоненты запущены!
echo [*] Для остановки закройте окна терминалов или нажмите Ctrl+C в каждом
pause