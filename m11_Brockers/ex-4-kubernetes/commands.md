# Шпаргалка команд Kubernetes 

## Основные команды

### Развертывание

```bash
# Применить манифест
kubectl apply -f deployment.yaml

# Применить все файлы в папке
kubectl apply -f .

# Удалить ресурсы
kubectl delete -f deployment.yaml
```

### Просмотр ресурсов

```bash
# Все поды
kubectl get pods

# Поды с подробностями
kubectl get pods -o wide

# Сервисы
kubectl get services

# Развертывания
kubectl get deployments

# Все ресурсы
kubectl get all
```

### Отладка

```bash
# Логи пода
kubectl logs chat-app-xxx

# Логи в реальном времени
kubectl logs -f chat-app-xxx

# Описание пода
kubectl describe pod chat-app-xxx

# Подключение к поду
kubectl exec -it chat-app-xxx -- sh
```

### Масштабирование

```bash
# Увеличить до 3 реплик
kubectl scale deployment chat-app --replicas=3

# Уменьшить до 1 реплики
kubectl scale deployment chat-app --replicas=1
```

### Доступ к приложению

```bash
# Проброс порта
kubectl port-forward service/chat-service 8080:80

# Проброс порта пода
kubectl port-forward pod/chat-app-xxx 8080:5000
```

## Полезные команды

### Мониторинг

```bash
# Следить за подами
kubectl get pods -w

# Использование ресурсов
kubectl top pods

# События кластера
kubectl get events
```

### Информация о кластере

```bash
# Информация о кластере
kubectl cluster-info

# Узлы кластера
kubectl get nodes

# Версия kubectl
kubectl version
```

## Быстрые команды для проекта

```bash
# 1. Сборка и развертывание
docker build -t chat-app:latest .
kubectl apply -f .

# 2. Проверка статуса
kubectl get pods
kubectl get services

# 3. Доступ к чату
kubectl port-forward service/chat-service 8080:80

# 4. Масштабирование
kubectl scale deployment chat-app --replicas=3

# 5. Просмотр логов
kubectl logs -l app=chat-app

# 6. Очистка
kubectl delete -f .
```
