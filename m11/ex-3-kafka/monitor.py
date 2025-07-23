import json
import time
import colorama
from colorama import Fore, Style
import os
import requests
import threading
import random
from datetime import datetime
from confluent_kafka.admin import AdminClient
from confluent_kafka import KafkaException

# Инициализация colorama для цветного вывода
colorama.init()

# Настройки Kafka
KAFKA_BOOTSTRAP_SERVERS = 'localhost:9092'
KAFKA_TOPIC = 'orders'
KAFKA_UI_PORT = 8080

# Глобальные переменные для имитации скорости
SIMULATED_PUBLISH_RATE = 0.0
SIMULATED_CONSUME_RATE = 0.0
SIMULATION_MODE = True  # Включение/выключение режима имитации

# Создание админ-клиента Kafka
try:
    admin_client = AdminClient({'bootstrap.servers': KAFKA_BOOTSTRAP_SERVERS})
except KafkaException as e:
    print(f"{Fore.RED}[!] Ошибка подключения к Kafka: {e}{Style.RESET_ALL}")
    admin_client = None

def clear_screen():
    """Очистка экрана в зависимости от ОС"""
    os.system('cls' if os.name == 'nt' else 'clear')

def get_topic_info():
    """Получение информации о топике Kafka"""
    global SIMULATED_PUBLISH_RATE, SIMULATED_CONSUME_RATE, SIMULATION_MODE
    
    # В режиме имитации или если нет подключения к Kafka
    if SIMULATION_MODE or admin_client is None:
        # Симулируем данные о топике
        # Разница между опубликованными и потребленными сообщениями
        lag = max(0, int(SIMULATED_PUBLISH_RATE * 5 - SIMULATED_CONSUME_RATE * 5))
        
        return {
            'topic': KAFKA_TOPIC,
            'partitions': 1,
            'messages_total': int(SIMULATED_PUBLISH_RATE * 10),  # Общее количество сообщений
            'messages_in_progress': int(SIMULATED_CONSUME_RATE * 2),  # Сообщения в обработке
            'messages_pending': lag,  # Ожидающие сообщения
            'publish_rate': SIMULATED_PUBLISH_RATE,
            'consume_rate': SIMULATED_CONSUME_RATE
        }
    
    # Реальный режим - попытка получить информацию из Kafka
    try:
        # Получаем информацию о топике через Kafka UI API
        url = f"http://localhost:{KAFKA_UI_PORT}/api/clusters/local/topics/{KAFKA_TOPIC}"
        response = requests.get(url)
        
        if response.status_code == 200:
            data = response.json()
            # Преобразуем данные в наш формат
            return {
                'topic': data.get('name', KAFKA_TOPIC),
                'partitions': len(data.get('partitions', [])),
                'messages_total': data.get('messagesCount', 0),
                'messages_in_progress': 0,  # Нет прямого аналога в Kafka
                'messages_pending': data.get('messagesCount', 0),  # Упрощенно
                'publish_rate': 0,  # Нет прямого аналога в API
                'consume_rate': 0   # Нет прямого аналога в API
            }
        else:
            # Если не удалось получить данные, используем имитацию
            print(f"{Fore.YELLOW}[!] Не удалось получить данные из Kafka UI API, используем имитацию{Style.RESET_ALL}")
            return get_topic_info()  # Рекурсивный вызов с имитацией
    except Exception as e:
        print(f"{Fore.RED}[!] Ошибка при получении данных о топике: {e}{Style.RESET_ALL}")
        # В случае ошибки используем имитацию
        return get_topic_info()  # Рекурсивный вызов с имитацией

def display_topic_stats():
    """Отображение статистики топика Kafka"""
    try:
        topic_info = get_topic_info()
        
        if not topic_info:
            print(f"{Fore.RED}[!] Не удалось получить информацию о топике{Style.RESET_ALL}")
            return
        
        # Очистка экрана перед выводом новой информации
        clear_screen()
        
        # Текущее время
        current_time = datetime.now().strftime("%H:%M:%S")
        
        # Заголовок
        print(f"{Fore.CYAN}╔{'═' * 60}╗{Style.RESET_ALL}")
        print(f"{Fore.CYAN}║{Style.RESET_ALL} {Fore.WHITE}МОНИТОР ТОПИКА KAFKA{Style.RESET_ALL}{' ' * 40}{Fore.CYAN}║{Style.RESET_ALL}")
        print(f"{Fore.CYAN}╠{'═' * 60}╣{Style.RESET_ALL}")
        
        # Основная информация
        messages_total = topic_info.get('messages_total', 0)
        messages_pending = topic_info.get('messages_pending', 0)
        messages_in_progress = topic_info.get('messages_in_progress', 0)
        partitions = topic_info.get('partitions', 1)
        
        # Статистика сообщений
        print(f"{Fore.CYAN}║{Style.RESET_ALL} Имя топика: {Fore.GREEN}{KAFKA_TOPIC}{Style.RESET_ALL}{' ' * (48 - len(KAFKA_TOPIC))}{Fore.CYAN}║{Style.RESET_ALL}")
        print(f"{Fore.CYAN}║{Style.RESET_ALL} Время обновления: {Fore.YELLOW}{current_time}{Style.RESET_ALL}{' ' * (43 - len(current_time))}{Fore.CYAN}║{Style.RESET_ALL}")
        print(f"{Fore.CYAN}║{Style.RESET_ALL} Количество партиций: {Fore.BLUE}{partitions}{Style.RESET_ALL}{' ' * (38 - len(str(partitions)))}{Fore.CYAN}║{Style.RESET_ALL}")
        print(f"{Fore.CYAN}╠{'═' * 60}╣{Style.RESET_ALL}")
        
        print(f"{Fore.CYAN}║{Style.RESET_ALL} {Fore.WHITE}СТАТИСТИКА СООБЩЕНИЙ:{Style.RESET_ALL}{' ' * 39}{Fore.CYAN}║{Style.RESET_ALL}")
        print(f"{Fore.CYAN}║{Style.RESET_ALL} Всего сообщений: {Fore.MAGENTA}{messages_total}{Style.RESET_ALL}{' ' * (42 - len(str(messages_total)))}{Fore.CYAN}║{Style.RESET_ALL}")
        print(f"{Fore.CYAN}║{Style.RESET_ALL} Ожидающие обработки: {Fore.GREEN}{messages_pending}{Style.RESET_ALL}{' ' * (36 - len(str(messages_pending)))}{Fore.CYAN}║{Style.RESET_ALL}")
        print(f"{Fore.CYAN}║{Style.RESET_ALL} В процессе обработки: {Fore.YELLOW}{messages_in_progress}{Style.RESET_ALL}{' ' * (37 - len(str(messages_in_progress)))}{Fore.CYAN}║{Style.RESET_ALL}")
        
        # Визуализация топика
        print(f"{Fore.CYAN}╠{'═' * 60}╣{Style.RESET_ALL}")
        print(f"{Fore.CYAN}║{Style.RESET_ALL} {Fore.WHITE}ВИЗУАЛИЗАЦИЯ ТОПИКА:{Style.RESET_ALL}{' ' * 40}{Fore.CYAN}║{Style.RESET_ALL}")
        
        # Создаем визуальное представление топика
        max_display = 50  # Максимальное количество символов для отображения
        
        if messages_total > 0:
            # Определяем сколько символов использовать для каждого типа сообщений
            if messages_total <= max_display:
                pending_chars = messages_pending
                in_progress_chars = messages_in_progress
            else:
                # Масштабируем, если сообщений больше чем можем отобразить
                scale = max_display / messages_total
                pending_chars = int(messages_pending * scale)
                in_progress_chars = int(messages_in_progress * scale)
                
                # Убедимся, что у нас есть хотя бы один символ для каждого типа, если они существуют
                if messages_pending > 0 and pending_chars == 0:
                    pending_chars = 1
                if messages_in_progress > 0 and in_progress_chars == 0:
                    in_progress_chars = 1
                    
                # Корректируем, если сумма превышает max_display
                if pending_chars + in_progress_chars > max_display:
                    if pending_chars > in_progress_chars:
                        pending_chars = max_display - in_progress_chars
                    else:
                        in_progress_chars = max_display - pending_chars
            
            # Создаем визуальное представление
            topic_visual = f"{Fore.GREEN}{'■' * pending_chars}{Fore.YELLOW}{'■' * in_progress_chars}{Style.RESET_ALL}"
            empty_space = ' ' * (max_display - pending_chars - in_progress_chars)
            
            print(f"{Fore.CYAN}║{Style.RESET_ALL} [{topic_visual}{empty_space}] {' ' * 7}{Fore.CYAN}║{Style.RESET_ALL}")
        else:
            print(f"{Fore.CYAN}║{Style.RESET_ALL} [{' ' * max_display}] {' ' * 7}{Fore.CYAN}║{Style.RESET_ALL}")
        
        # Легенда
        print(f"{Fore.CYAN}║{Style.RESET_ALL} {Fore.GREEN}■{Style.RESET_ALL} - Ожидающие обработки   {Fore.YELLOW}■{Style.RESET_ALL} - В процессе обработки {' ' * 7}{Fore.CYAN}║{Style.RESET_ALL}")
        
        # Статистика производительности
        print(f"{Fore.CYAN}╠{'═' * 60}╣{Style.RESET_ALL}")
        print(f"{Fore.CYAN}║{Style.RESET_ALL} {Fore.WHITE}ПРОИЗВОДИТЕЛЬНОСТЬ:{Style.RESET_ALL}{' ' * 42}{Fore.CYAN}║{Style.RESET_ALL}")
        
        # Получаем статистику по скорости обработки
        publish_rate = topic_info.get('publish_rate', 0)
        consume_rate = topic_info.get('consume_rate', 0)
        
        print(f"{Fore.CYAN}║{Style.RESET_ALL} Скорость публикации: {Fore.BLUE}{publish_rate:.2f} сообщ/сек{Style.RESET_ALL}{' ' * (30 - len(f'{publish_rate:.2f}'))}{Fore.CYAN}║{Style.RESET_ALL}")
        print(f"{Fore.CYAN}║{Style.RESET_ALL} Скорость обработки: {Fore.GREEN}{consume_rate:.2f} сообщ/сек{Style.RESET_ALL}{' ' * (30 - len(f'{consume_rate:.2f}'))}{Fore.CYAN}║{Style.RESET_ALL}")
        
        # Нижняя граница таблицы
        print(f"{Fore.CYAN}╚{'═' * 60}╝{Style.RESET_ALL}")
        
    except Exception as e:
        print(f"{Fore.RED}[!] Ошибка при отображении статистики: {e}{Style.RESET_ALL}")

def simulate_rates():
    """Функция для имитации разной скорости обработки заказов"""
    global SIMULATED_PUBLISH_RATE, SIMULATED_CONSUME_RATE, SIMULATION_MODE
    
    if not SIMULATION_MODE:
        return
        
    # Сценарии имитации
    scenarios = [
        # Нормальная работа - публикация и обработка примерно одинаковые
        lambda: (random.uniform(1.0, 3.0), random.uniform(1.0, 3.0)),
        
        # Высокая нагрузка - много публикаций, медленная обработка
        lambda: (random.uniform(5.0, 10.0), random.uniform(0.5, 2.0)),
        
        # Быстрая обработка - мало публикаций, быстрая обработка
        lambda: (random.uniform(0.5, 2.0), random.uniform(3.0, 8.0)),
        
        # Пиковая нагрузка - очень много публикаций
        lambda: (random.uniform(15.0, 25.0), random.uniform(5.0, 10.0)),
        
        # Простой - почти нет активности
        lambda: (random.uniform(0.0, 0.5), random.uniform(0.0, 0.5))
    ]
    
    while SIMULATION_MODE:
        # Выбираем случайный сценарий
        scenario = random.choice(scenarios)
        publish_rate, consume_rate = scenario()
        
        # Плавно изменяем скорость в течение нескольких секунд
        steps = 10
        old_publish_rate = SIMULATED_PUBLISH_RATE
        old_consume_rate = SIMULATED_CONSUME_RATE
        
        for i in range(steps):
            # Плавно изменяем скорость
            SIMULATED_PUBLISH_RATE = old_publish_rate + (publish_rate - old_publish_rate) * (i + 1) / steps
            SIMULATED_CONSUME_RATE = old_consume_rate + (consume_rate - old_consume_rate) * (i + 1) / steps
            time.sleep(0.5)
        
        # Сохраняем скорость на некоторое время
        time.sleep(random.uniform(3.0, 8.0))

def main():
    """Основная функция мониторинга"""
    global SIMULATION_MODE
    
    print(f"{Fore.BLUE}[*] Запуск монитора топика Kafka...{Style.RESET_ALL}")
    print(f"{Fore.BLUE}[*] Подключение к {KAFKA_BOOTSTRAP_SERVERS}, топик: {KAFKA_TOPIC}{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}[*] Режим имитации скорости: {'Включен' if SIMULATION_MODE else 'Выключен'}{Style.RESET_ALL}")
    print(f"{Fore.BLUE}[*] Для выхода нажмите CTRL+C{Style.RESET_ALL}")
    
    # Запускаем поток для имитации скорости
    if SIMULATION_MODE:
        simulation_thread = threading.Thread(target=simulate_rates, daemon=True)
        simulation_thread.start()
    
    try:
        while True:
            display_topic_stats()
            time.sleep(1)  # Обновление каждую секунду
    except KeyboardInterrupt:
        print(f"\n{Fore.RED}[!] Мониторинг остановлен{Style.RESET_ALL}")
        SIMULATION_MODE = False  # Останавливаем поток имитации

if __name__ == "__main__":
    main()