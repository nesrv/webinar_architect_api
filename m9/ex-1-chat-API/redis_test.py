import redis
import sys

def test_redis_connection():
    """Проверяет подключение к Redis и выводит статус"""
    try:
        # Пытаемся подключиться к Redis
        r = redis.Redis(host='localhost', port=6380, decode_responses=True)
        
        # Проверяем соединение с помощью ping
        response = r.ping()
        
        if response:
            print("✅ Соединение с Redis установлено успешно!")
            
            # Проверяем работу pub/sub
            pubsub = r.pubsub()
            pubsub.subscribe("test_channel")
            
            # Публикуем тестовое сообщение
            r.publish("test_channel", "Тестовое сообщение")
            
            # Получаем сообщение
            message = pubsub.get_message()
            if message:
                print("✅ Механизм pub/sub работает корректно")
            
            # Отписываемся
            pubsub.unsubscribe("test_channel")
            
            print("\nRedis готов к использованию в чат-приложении!")
            return True
        else:
            print("❌ Ошибка: Redis не отвечает на ping")
            return False
    except redis.ConnectionError:
        print("❌ Ошибка подключения к Redis")
        print("Убедитесь, что Redis запущен на localhost:6379")
        return False
    except Exception as e:
        print(f"❌ Неизвестная ошибка: {e}")
        return False

if __name__ == "__main__":
    print("Проверка подключения к Redis...")
    success = test_redis_connection()
    
    if not success:
        print("\nРекомендации:")
        print("1. Убедитесь, что Redis установлен")
        print("2. Проверьте, что Redis сервер запущен")
        print("3. Проверьте, что Redis доступен на localhost:6379")
        sys.exit(1)
    
    sys.exit(0)