# Импортируем необходимые компоненты из библиотеки spyne
from spyne import Application, rpc, ServiceBase, Integer, Unicode
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication

# Определяем класс сервиса, который наследуется от ServiceBase
class UserService(ServiceBase):
    # Метод для получения информации о пользователе по ID
    # @rpc декоратор указывает, что метод будет доступен через SOAP
    # Integer - тип входного параметра, _returns=Unicode - тип возвращаемого значения
    @rpc(Integer, _returns=Unicode)
    def get_user(ctx, user_id):
        # Словарь с данными пользователей (в реальном приложении здесь был бы запрос к БД)
        users = {1: "Alice", 2: "Bob"}
        # Возвращаем имя пользователя или сообщение, если пользователь не найден
        return users.get(user_id, "User not found")

    # Метод для создания нового пользователя
    # Принимает имя пользователя и возвращает сообщение о создании
    @rpc(Unicode, _returns=Unicode)
    def create_user(ctx, name):
        # В реальном приложении здесь был бы код для сохранения пользователя в БД
        return f"User {name} created"

# Создаем SOAP приложение
application = Application(
    [UserService],  # Список сервисов, которые будут доступны
    tns="http://example.com/user-service",  # Пространство имен сервиса
    in_protocol=Soap11(validator="lxml"),  # Протокол для входящих сообщений с валидацией через lxml
    out_protocol=Soap11(),  # Протокол для исходящих сообщений
)

# Создаем WSGI-приложение для запуска SOAP-сервиса
# Это приложение можно запустить с помощью любого WSGI-сервера (например, Gunicorn, uWSGI)
soap_app = WsgiApplication(application)