# Импортируем необходимые компоненты из FastAPI и библиотеки zeep для работы с SOAP
from fastapi import FastAPI, HTTPException
from zeep import Client

# Создаем экземпляр FastAPI приложения
app = FastAPI()
SOAP_URL = "http://localhost:8000/soap"  # Эндпоинт SOAP-сервиса

# Создаем клиент для SOAP-сервиса с использованием библиотеки zeep
# ?wsdl - запрашивает WSDL-документ, описывающий интерфейс сервиса
soap_client = Client(f"{SOAP_URL}?wsdl")

# Определяем GET-эндпоинт для получения информации о пользователе по ID
@app.get("/user/{user_id}")
async def get_user(user_id: int):
    try:
        # Вызываем метод get_user SOAP-сервиса через клиент zeep
        result = soap_client.service.get_user(user_id)
        # Возвращаем результат в формате JSON
        return {"user": result}
    except Exception as e:
        # В случае ошибки возвращаем HTTP-ошибку с описанием проблемы
        raise HTTPException(status_code=400, detail=str(e))

# Определяем POST-эндпоинт для создания нового пользователя
@app.post("/user")
async def create_user(name: str):
    try:
        # Вызываем метод create_user SOAP-сервиса через клиент zeep
        result = soap_client.service.create_user(name)
        # Возвращаем сообщение о результате операции
        return {"message": result}
    except Exception as e:
        # В случае ошибки возвращаем HTTP-ошибку с описанием проблемы
        raise HTTPException(status_code=400, detail=str(e))