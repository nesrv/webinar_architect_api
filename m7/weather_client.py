import grpc
import weather_pb2
import weather_pb2_grpc
import time
import datetime
import threading
import random
import logging
from google.protobuf.json_format import MessageToDict

# Настройка логирования
logging.basicConfig(level=logging.INFO)

def get_current_weather(stub, city, country_code=""):
    """Получить текущую погоду"""
    try:
        response = stub.GetCurrentWeather(
            weather_pb2.CityRequest(city=city, country_code=country_code)
        )
        
        print("\n=== ТЕКУЩАЯ ПОГОДА ===")
        print(f"Город: {response.city}, {response.country}")
        print(f"Температура: {response.temperature}°C (ощущается как {response.feels_like}°C)")
        print(f"Влажность: {response.humidity}%")
        print(f"Ветер: {response.wind_speed} м/с")
        print(f"Погодные условия: {response.condition}")
        print(f"Время измерения: {datetime.datetime.fromtimestamp(response.timestamp)}")
        
        return response
    except grpc.RpcError as e:
        print(f"Ошибка при получении погоды: {e.details()}")
        return None

def get_forecast(stub, city, days=3, country_code=""):
    """Получить прогноз погоды на несколько дней"""
    try:
        response = stub.GetForecast(
            weather_pb2.ForecastRequest(city=city, country_code=country_code, days=days)
        )
        
        print(f"\n=== ПРОГНОЗ ПОГОДЫ НА {len(response.daily)} ДНЕЙ ===")
        print(f"Город: {response.city}, {response.country}")
        
        for i, day in enumerate(response.daily):
            date = datetime.datetime.fromtimestamp(day.date).strftime("%d.%m.%Y")
            print(f"\nДень {i+1} ({date}):")
            print(f"  Температура: {day.temp_min}°C - {day.temp_max}°C")
            print(f"  Влажность: {day.humidity}%")
            print(f"  Ветер: {day.wind_speed} м/с")
            print(f"  Погодные условия: {day.condition}")
            print(f"  Вероятность осадков: {day.precipitation_chance}%")
        
        return response
    except grpc.RpcError as e:
        print(f"Ошибка при получении прогноза: {e.details()}")
        return None

def subscribe_to_weather_updates(stub, city, country_code=""):
    """Подписаться на обновления погоды"""
    try:
        request = weather_pb2.CityRequest(city=city, country_code=country_code)
        
        print(f"\n=== ПОДПИСКА НА ОБНОВЛЕНИЯ ПОГОДЫ ДЛЯ {city} ===")
        print("Нажмите Ctrl+C для отмены подписки")
        
        for update in stub.SubscribeToWeatherUpdates(request):
            print(f"\nОбновление погоды ({datetime.datetime.fromtimestamp(update.timestamp)}):")
            print(f"  Температура: {update.temperature}°C (ощущается как {update.feels_like}°C)")
            print(f"  Влажность: {update.humidity}%")
            print(f"  Ветер: {update.wind_speed} м/с")
            print(f"  Погодные условия: {update.condition}")
    except grpc.RpcError as e:
        print(f"Ошибка в подписке: {e.details()}")
    except KeyboardInterrupt:
        print("\nПодписка отменена пользователем")

def send_weather_data(stub):
    """Отправить данные с метеостанции"""
    try:
        # Генерируем случайный ID станции
        station_id = f"STATION-{random.randint(1000, 9999)}"
        
        print(f"\n=== ОТПРАВКА ДАННЫХ С МЕТЕОСТАНЦИИ {station_id} ===")
        
        # Функция для создания данных о погоде
        def generate_weather_data():
            return weather_pb2.WeatherData(
                station_id=station_id,
                latitude=random.uniform(55.0, 56.0),  # Примерно Москва
                longitude=random.uniform(37.0, 38.0),
                temperature=random.uniform(10.0, 25.0),
                humidity=random.uniform(40.0, 90.0),
                pressure=random.uniform(990.0, 1020.0),
                wind_speed=random.uniform(0.0, 10.0),
                wind_direction=random.uniform(0.0, 360.0),
                rainfall=random.uniform(0.0, 5.0),
                timestamp=int(time.time())
            )
        
        # Создаем генератор данных
        def data_generator():
            for _ in range(5):  # Отправляем 5 записей
                data = generate_weather_data()
                print(f"Отправка данных: Температура={data.temperature:.1f}°C, Влажность={data.humidity:.1f}%")
                yield data
                time.sleep(1)
        
        # Отправляем данные и получаем ответ
        response = stub.SendWeatherData(data_generator())
        
        print("\nРезультат отправки данных:")
        print(f"Успех: {response.success}")
        print(f"Сообщение: {response.message}")
        print(f"Обработано записей: {response.records_processed}")
        
        return response
    except grpc.RpcError as e:
        print(f"Ошибка при отправке данных: {e.details()}")
        return None

def chat_with_meteorologist(stub):
    """Чат с метеорологом"""
    try:
        print("\n=== ЧАТ С МЕТЕОРОЛОГОМ ===")
        print("Введите 'выход' для завершения чата")
        
        # Создаем двунаправленный стрим
        chat_stream = stub.ChatWithMeteorologist()
        
        # Запускаем поток для получения сообщений от метеоролога
        def receive_messages():
            try:
                for message in chat_stream:
                    timestamp = datetime.datetime.fromtimestamp(message.timestamp).strftime("%H:%M:%S")
                    print(f"\n[{timestamp}] {message.user_id}: {message.message}")
            except grpc.RpcError as e:
                if e.code() != grpc.StatusCode.CANCELLED:
                    print(f"Ошибка при получении сообщений: {e.details()}")
        
        # Запускаем поток для получения сообщений
        thread = threading.Thread(target=receive_messages)
        thread.daemon = True
        thread.start()
        
        # Генерируем случайный ID пользователя
        user_id = f"User-{random.randint(1000, 9999)}"
        
        # Отправляем сообщения
        try:
            while True:
                user_input = input("\nВведите сообщение: ")
                
                if user_input.lower() == 'выход':
                    break
                
                # Отправляем сообщение
                chat_stream.add(weather_pb2.ChatMessage(
                    user_id=user_id,
                    message=user_input,
                    timestamp=int(time.time()),
                    is_meteorologist=False
                ))
                
                # Небольшая пауза для получения ответа
                time.sleep(0.5)
        finally:
            # Закрываем стрим
            chat_stream.cancel()
            print("\nЧат завершен")
    except grpc.RpcError as e:
        print(f"Ошибка в чате: {e.details()}")

def run():
    """Основная функция для запуска клиента"""
    # Устанавливаем соединение с сервером
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = weather_pb2_grpc.WeatherServiceStub(channel)
        
        while True:
            print("\n=== КЛИЕНТ СЕРВИСА ПРОГНОЗА ПОГОДЫ ===")
            print("1. Получить текущую погоду")
            print("2. Получить прогноз погоды")
            print("3. Подписаться на обновления погоды")
            print("4. Отправить данные с метеостанции")
            print("5. Чат с метеорологом")
            print("0. Выход")
            
            choice = input("\nВыберите опцию: ")
            
            if choice == '1':
                city = input("Введите название города: ")
                get_current_weather(stub, city)
            elif choice == '2':
                city = input("Введите название города: ")
                days = int(input("Введите количество дней (1-7): "))
                get_forecast(stub, city, days)
            elif choice == '3':
                city = input("Введите название города: ")
                subscribe_to_weather_updates(stub, city)
            elif choice == '4':
                send_weather_data(stub)
            elif choice == '5':
                chat_with_meteorologist(stub)
            elif choice == '0':
                print("До свидания!")
                break
            else:
                print("Неверный выбор. Попробуйте снова.")

if __name__ == '__main__':
    run()