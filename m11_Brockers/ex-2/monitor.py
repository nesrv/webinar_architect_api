import pika
import json
import time
import colorama
from colorama import Fore, Style
import os
import requests
from datetime import datetime

# Инициализация colorama для цветного вывода
colorama.init()

# Настройки RabbitMQ
RABBITMQ_HOST = 'localhost'
RABBITMQ_PORT = 15672
RABBITMQ_USER = 'guest'
RABBITMQ_PASS = 'guest'
QUEUE_NAME = 'orders'

def clear_screen():
    """Очистка экрана в зависимости от ОС"""
    os.system('cls' if os.name == 'nt' else 'clear')

def get_queue_info():
    """Получение информации о состоянии очереди через RabbitMQ API"""
    try:
        url = f"http://{RABBITMQ_HOST}:{RABBITMQ_PORT}/api/queues/%2F/{QUEUE_NAME}"
        response = requests.get(url, auth=(RABBITMQ_USER, RABBITMQ_PASS))
        
        if response.status_code == 200:
            return response.json()
        else:
            print(f"{Fore.RED}[!] Ошибка API RabbitMQ: {response.status_code} - {response.text}{Style.RESET_ALL}")
            return {
                'messages': 0,
                'messages_ready': 0,
                'messages_unacknowledged': 0,
                'message_stats': {
                    'publish_details': {'rate': 0},
                    'deliver_details': {'rate': 0}
                }
            }
    except Exception as e:
        print(f"{Fore.RED}[!] Ошибка при получении данных из RabbitMQ API: {e}{Style.RESET_ALL}")
        return {
            'messages': 0,
            'messages_ready': 0,
            'messages_unacknowledged': 0,
            'message_stats': {
                'publish_details': {'rate': 0},
                'deliver_details': {'rate': 0}
            }
        }

def display_queue_stats():
    """Отображение статистики очереди"""
    try:
        queue_info = get_queue_info()
        
        if not queue_info:
            print(f"{Fore.RED}[!] Не удалось получить информацию о очереди{Style.RESET_ALL}")
            return
        
        # Очистка экрана перед выводом новой информации
        clear_screen()
        
        # Текущее время
        current_time = datetime.now().strftime("%H:%M:%S")
        
        # Заголовок
        print(f"{Fore.CYAN}╔{'═' * 60}╗{Style.RESET_ALL}")
        print(f"{Fore.CYAN}║{Style.RESET_ALL} {Fore.WHITE}МОНИТОР ОЧЕРЕДИ RABBITMQ{Style.RESET_ALL}{' ' * 38}{Fore.CYAN}║{Style.RESET_ALL}")
        print(f"{Fore.CYAN}╠{'═' * 60}╣{Style.RESET_ALL}")
        
        # Основная информация
        messages = queue_info.get('messages', 0)
        messages_ready = queue_info.get('messages_ready', 0)
        messages_unacked = queue_info.get('messages_unacknowledged', 0)
        
        # Статистика сообщений
        print(f"{Fore.CYAN}║{Style.RESET_ALL} Имя очереди: {Fore.GREEN}{QUEUE_NAME}{Style.RESET_ALL}{' ' * (48 - len(QUEUE_NAME))}{Fore.CYAN}║{Style.RESET_ALL}")
        print(f"{Fore.CYAN}║{Style.RESET_ALL} Время обновления: {Fore.YELLOW}{current_time}{Style.RESET_ALL}{' ' * (43 - len(current_time))}{Fore.CYAN}║{Style.RESET_ALL}")
        print(f"{Fore.CYAN}╠{'═' * 60}╣{Style.RESET_ALL}")
        
        print(f"{Fore.CYAN}║{Style.RESET_ALL} {Fore.WHITE}СТАТИСТИКА СООБЩЕНИЙ:{Style.RESET_ALL}{' ' * 39}{Fore.CYAN}║{Style.RESET_ALL}")
        print(f"{Fore.CYAN}║{Style.RESET_ALL} Всего сообщений: {Fore.MAGENTA}{messages}{Style.RESET_ALL}{' ' * (42 - len(str(messages)))}{Fore.CYAN}║{Style.RESET_ALL}")
        print(f"{Fore.CYAN}║{Style.RESET_ALL} Готовы к обработке: {Fore.GREEN}{messages_ready}{Style.RESET_ALL}{' ' * (39 - len(str(messages_ready)))}{Fore.CYAN}║{Style.RESET_ALL}")
        print(f"{Fore.CYAN}║{Style.RESET_ALL} В процессе обработки: {Fore.YELLOW}{messages_unacked}{Style.RESET_ALL}{' ' * (37 - len(str(messages_unacked)))}{Fore.CYAN}║{Style.RESET_ALL}")
        
        # Визуализация очереди
        print(f"{Fore.CYAN}╠{'═' * 60}╣{Style.RESET_ALL}")
        print(f"{Fore.CYAN}║{Style.RESET_ALL} {Fore.WHITE}ВИЗУАЛИЗАЦИЯ ОЧЕРЕДИ:{Style.RESET_ALL}{' ' * 39}{Fore.CYAN}║{Style.RESET_ALL}")
        
        # Создаем визуальное представление очереди
        max_display = 50  # Максимальное количество символов для отображения
        
        if messages > 0:
            # Определяем сколько символов использовать для каждого типа сообщений
            if messages <= max_display:
                ready_chars = messages_ready
                unacked_chars = messages_unacked
            else:
                # Масштабируем, если сообщений больше чем можем отобразить
                scale = max_display / messages
                ready_chars = int(messages_ready * scale)
                unacked_chars = int(messages_unacked * scale)
                
                # Убедимся, что у нас есть хотя бы один символ для каждого типа, если они существуют
                if messages_ready > 0 and ready_chars == 0:
                    ready_chars = 1
                if messages_unacked > 0 and unacked_chars == 0:
                    unacked_chars = 1
                    
                # Корректируем, если сумма превышает max_display
                if ready_chars + unacked_chars > max_display:
                    if ready_chars > unacked_chars:
                        ready_chars = max_display - unacked_chars
                    else:
                        unacked_chars = max_display - ready_chars
            
            # Создаем визуальное представление
            queue_visual = f"{Fore.GREEN}{'■' * ready_chars}{Fore.YELLOW}{'■' * unacked_chars}{Style.RESET_ALL}"
            empty_space = ' ' * (max_display - ready_chars - unacked_chars)
            
            print(f"{Fore.CYAN}║{Style.RESET_ALL} [{queue_visual}{empty_space}] {' ' * 7}{Fore.CYAN}║{Style.RESET_ALL}")
        else:
            print(f"{Fore.CYAN}║{Style.RESET_ALL} [{' ' * max_display}] {' ' * 7}{Fore.CYAN}║{Style.RESET_ALL}")
        
        # Легенда
        print(f"{Fore.CYAN}║{Style.RESET_ALL} {Fore.GREEN}■{Style.RESET_ALL} - Готовы к обработке   {Fore.YELLOW}■{Style.RESET_ALL} - В процессе обработки {' ' * 7}{Fore.CYAN}║{Style.RESET_ALL}")
        
        # Статистика производительности
        print(f"{Fore.CYAN}╠{'═' * 60}╣{Style.RESET_ALL}")
        print(f"{Fore.CYAN}║{Style.RESET_ALL} {Fore.WHITE}ПРОИЗВОДИТЕЛЬНОСТЬ:{Style.RESET_ALL}{' ' * 42}{Fore.CYAN}║{Style.RESET_ALL}")
        
        # Получаем статистику по скорости обработки
        message_stats = queue_info.get('message_stats', {})
        publish_rate = message_stats.get('publish_details', {}).get('rate', 0)
        deliver_rate = message_stats.get('deliver_details', {}).get('rate', 0)
        
        print(f"{Fore.CYAN}║{Style.RESET_ALL} Скорость публикации: {Fore.BLUE}{publish_rate:.2f} сообщ/сек{Style.RESET_ALL}{' ' * (30 - len(f'{publish_rate:.2f}'))}{Fore.CYAN}║{Style.RESET_ALL}")
        print(f"{Fore.CYAN}║{Style.RESET_ALL} Скорость обработки: {Fore.GREEN}{deliver_rate:.2f} сообщ/сек{Style.RESET_ALL}{' ' * (30 - len(f'{deliver_rate:.2f}'))}{Fore.CYAN}║{Style.RESET_ALL}")
        
        # Нижняя граница таблицы
        print(f"{Fore.CYAN}╚{'═' * 60}╝{Style.RESET_ALL}")
        
    except Exception as e:
        print(f"{Fore.RED}[!] Ошибка при отображении статистики: {e}{Style.RESET_ALL}")

def main():
    """Основная функция мониторинга"""
    print(f"{Fore.BLUE}[*] Запуск монитора очереди RabbitMQ...{Style.RESET_ALL}")
    print(f"{Fore.BLUE}[*] Подключение к {RABBITMQ_HOST}:{RABBITMQ_PORT}, очередь: {QUEUE_NAME}{Style.RESET_ALL}")
    print(f"{Fore.BLUE}[*] Для выхода нажмите CTRL+C{Style.RESET_ALL}")
    
    try:
        while True:
            display_queue_stats()
            time.sleep(1)  # Обновление каждую секунду
    except KeyboardInterrupt:
        print(f"\n{Fore.RED}[!] Мониторинг остановлен{Style.RESET_ALL}")

if __name__ == "__main__":
    main()