import grpc
import weather_pb2
import weather_pb2_grpc
from concurrent import futures
import time
import datetime
import random
import threading
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Имитация базы данных с погодой
WEATHER_DB = {
    "Москва": {
        "country": "Россия",
        "base_temp": 15,
        "condition": ["Ясно", "Облачно", "Дождь", "Переменная облачность"],
        "humidity": 65,
        "wind_speed": 3.5
    },
    "Санкт-Петербург": {
        "country": "Россия",
        "base_temp": 12,
        "condition": ["Облачно", "Дождь", "Туман", "Переменная облачность"],
        "humidity": 75,
        "wind_speed": 4.2
    },
    "Нью-Йорк": {
        "country": "США",
        "base_temp": 18,
        "condition": ["Ясно", "Облачно", "Гроза", "Переменная облачность"],
        "humidity": 60,
        "wind_speed": 5.0
    },
    "Лондон": {
        "country": "Великобритания",
        "base_temp": 14,
        "condition": ["Туман", "Дождь", "Облачно", "Переменная облачность"],
        "humidity": 80,
        "wind_speed": 4.8
    },
    "Токио": {
        "country": "Япония",
        "base_temp": 22,
        "condition": ["Ясно", "Дождь", "Облачно", "Переменная облачность"],
        "humidity": 70,
        "wind_speed": 3.2
    }
}

# Имитация метеорологов для чата
METEOROLOGISTS = ["Иван Петрович", "Мария Ивановна", "Алексей Сергеевич"]

class WeatherServiceServicer(weather_pb2_grpc.WeatherServiceServicer):
    """Реализация сервиса прогноза погоды"""
    
    def __init__(self):
        # Словарь для хранения активных подписок на обновления погоды
        self.weather_subscribers = {}
        # Словарь для хранения активных чатов
        self.active_chats = {}
    
    def GetCurrentWeather(self, request, context):
        """Получить текущую погоду по городу"""
        city = request.city
        logging.info(f"Запрос текущей погоды для города: {city}")
        
        if city not in WEATHER_DB:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details(f"Город {city} не найден в базе данных")
            return weather_pb2.WeatherResponse()
        
        city_data = WEATHER_DB[city]
        
        # Генерируем случайные вариации погоды на основе базовых данных
        temp_variation = random.uniform(-3, 3)
        temperature = city_data["base_temp"] + temp_variation
        feels_like = temperature - random.uniform(0, 2)
        humidity = city_data["humidity"] + random.uniform(-10, 10)
        wind_speed = city_data["wind_speed"] + random.uniform(-1, 1)
        condition = random.choice(city_data["condition"])
        
        return weather_pb2.WeatherResponse(
            city=city,
            country=city_data["country"],
            temperature=round(temperature, 1),
            feels_like=round(feels_like, 1),
            humidity=round(humidity, 1),
            wind_speed=round(wind_speed, 1),
            condition=condition,
            timestamp=int(time.time())
        )
    
    def GetForecast(self, request, context):
        """Получить прогноз погоды на несколько дней"""
        city = request.city
        days = min(request.days, 7)  # Максимум 7 дней
        
        logging.info(f"Запрос прогноза погоды для города {city} на {days} дней")
        
        if city not in WEATHER_DB:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details(f"Город {city} не найден в базе данных")
            return weather_pb2.ForecastResponse()
        
        city_data = WEATHER_DB[city]
        daily_forecasts = []
        
        # Текущая дата
        current_date = datetime.datetime.now()
        
        # Генерируем прогноз на каждый день
        for day in range(days):
            forecast_date = current_date + datetime.timedelta(days=day)
            
            # Генерируем случайные данные для прогноза
            base_temp = city_data["base_temp"] + random.uniform(-2, 2) * (day + 1)
            temp_min = base_temp - random.uniform(2, 5)
            temp_max = base_temp + random.uniform(2, 5)
            humidity = city_data["humidity"] + random.uniform(-15, 15)
            wind_speed = city_data["wind_speed"] + random.uniform(-2, 2)
            condition = random.choice(city_data["condition"])
            precipitation = random.uniform(0, 100) if "Дождь" in condition or "Гроза" in condition else random.uniform(0, 30)
            
            daily_forecast = weather_pb2.DailyForecast(
                date=int(forecast_date.timestamp()),
                temp_min=round(temp_min, 1),
                temp_max=round(temp_max, 1),
                humidity=round(humidity, 1),
                wind_speed=round(wind_speed, 1),
                condition=condition,
                precipitation_chance=round(precipitation, 1)
            )
            
            daily_forecasts.append(daily_forecast)
        
        return weather_pb2.ForecastResponse(
            city=city,
            country=city_data["country"],
            daily=daily_forecasts
        )
    
    def SubscribeToWeatherUpdates(self, request, context):
        """Подписаться на обновления погоды (стриминг с сервера)"""
        city = request.city
        
        logging.info(f"Новая подписка на обновления погоды для города: {city}")
        
        if city not in WEATHER_DB:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details(f"Город {city} не найден в базе данных")
            return
        
        # Добавляем обработчик для отмены подписки при закрытии соединения
        subscription_key = f"{city}_{time.time()}"
        context.add_callback(lambda: self._remove_subscriber(subscription_key))
        
        # Отправляем обновления погоды каждые 5 секунд
        while context.is_active():
            # Генерируем случайные данные о погоде
            city_data = WEATHER_DB[city]
            temp_variation = random.uniform(-3, 3)
            temperature = city_data["base_temp"] + temp_variation
            feels_like = temperature - random.uniform(0, 2)
            humidity = city_data["humidity"] + random.uniform(-10, 10)
            wind_speed = city_data["wind_speed"] + random.uniform(-1, 1)
            condition = random.choice(city_data["condition"])
            
            weather_update = weather_pb2.WeatherResponse(
                city=city,
                country=city_data["country"],
                temperature=round(temperature, 1),
                feels_like=round(feels_like, 1),
                humidity=round(humidity, 1),
                wind_speed=round(wind_speed, 1),
                condition=condition,
                timestamp=int(time.time())
            )
            
            yield weather_update
            time.sleep(5)
    
    def _remove_subscriber(self, subscription_key):
        """Удалить подписчика при закрытии соединения"""
        if subscription_key in self.weather_subscribers:
            del self.weather_subscribers[subscription_key]
            logging.info(f"Подписка {subscription_key} удалена")
    
    def SendWeatherData(self, request_iterator, context):
        """Обработка данных с метеостанции (стриминг на сервер)"""
        records_processed = 0
        
        for data in request_iterator:
            # Обрабатываем полученные данные
            station_id = data.station_id
            timestamp = datetime.datetime.fromtimestamp(data.timestamp)
            
            logging.info(f"Получены данные с метеостанции {station_id} от {timestamp}")
            logging.info(f"  Температура: {data.temperature}°C, Влажность: {data.humidity}%")
            logging.info(f"  Давление: {data.pressure} гПа, Ветер: {data.wind_speed} м/с")
            
            # Здесь можно добавить логику сохранения данных в базу
            
            records_processed += 1
        
        return weather_pb2.DataResponse(
            success=True,
            message=f"Успешно обработано {records_processed} записей с метеостанции",
            records_processed=records_processed
        )
    
    def ChatWithMeteorologist(self, request_iterator, context):
        """Чат с метеорологом (двунаправленный стриминг)"""
        # Выбираем случайного метеоролога для чата
        meteorologist = random.choice(METEOROLOGISTS)
        chat_id = str(time.time())
        
        logging.info(f"Начат новый чат {chat_id} с метеорологом {meteorologist}")
        
        # Отправляем приветственное сообщение
        yield weather_pb2.ChatMessage(
            user_id=meteorologist,
            message=f"Здравствуйте! Меня зовут {meteorologist}. Чем я могу вам помочь с прогнозом погоды?",
            timestamp=int(time.time()),
            is_meteorologist=True
        )
        
        # Обрабатываем входящие сообщения
        for message in request_iterator:
            user_id = message.user_id
            user_message = message.message
            
            logging.info(f"Чат {chat_id}: Получено сообщение от {user_id}: {user_message}")
            
            # Генерируем ответ метеоролога
            response = self._generate_meteorologist_response(user_message, meteorologist)
            
            # Отправляем ответ
            yield weather_pb2.ChatMessage(
                user_id=meteorologist,
                message=response,
                timestamp=int(time.time()),
                is_meteorologist=True
            )
    
    def _generate_meteorologist_response(self, user_message, meteorologist):
        """Генерирует ответ метеоролога на основе сообщения пользователя"""
        user_message = user_message.lower()
        
        # Простая логика для генерации ответов
        if "прогноз" in user_message:
            return "Прогноз погоды на ближайшие дни показывает переменную облачность с возможными осадками. Рекомендую следить за обновлениями."
        elif "дождь" in user_message:
            return "По нашим данным, вероятность осадков в ближайшие дни составляет около 40%. Рекомендую взять с собой зонт."
        elif "температура" in user_message:
            return "Температура воздуха будет колебаться в пределах 15-20 градусов Цельсия. Ночью возможно похолодание до 10 градусов."
        elif "ветер" in user_message:
            return "Ожидается умеренный ветер, 3-5 м/с, преимущественно северо-западного направления."
        elif "спасибо" in user_message:
            return "Всегда рад помочь! Если у вас возникнут еще вопросы о погоде, обращайтесь."
        else:
            return f"Я, {meteorologist}, готов ответить на ваши вопросы о погоде. Что именно вас интересует: прогноз, температура, осадки или ветер?"

def serve():
    """Запуск gRPC сервера"""
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    weather_pb2_grpc.add_WeatherServiceServicer_to_server(
        WeatherServiceServicer(), server
    )
    server.add_insecure_port('[::]:50051')
    server.start()
    logging.info("Сервер запущен на порту 50051")
    
    try:
        # Держим сервер запущенным
        while True:
            time.sleep(86400)  # 1 день
    except KeyboardInterrupt:
        server.stop(0)
        logging.info("Сервер остановлен")

if __name__ == '__main__':
    serve()