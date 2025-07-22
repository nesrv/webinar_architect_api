@echo off
echo Генерация кода Python из proto-файла...
python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. weather.proto
echo Готово!
pause