# Простой чат на Kubernetes

Максимально простой проект для изучения основ Kubernetes.

## Что включено

- **FastAPI приложение** - простой чат с веб-интерфейсом
- **Docker контейнер** - упаковка приложения
- **Kubernetes манифесты** - развертывание в кластере

## Быстрый старт

### 1. Сборка Docker образа

```bash
docker build -t chat-app:latest .
```

### 2. Развертывание в Kubernetes

```bash
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml
```

### 3. Проверка статуса

```bash
kubectl get pods
kubectl get services
```

### 4. Доступ к приложению

```bash
kubectl port-forward service/chat-service 8080:80
```

Откройте: http://localhost:8080

## Основные команды Kubernetes

### Просмотр ресурсов:

```bash
kubectl get pods          # Список подов
kubectl get services      # Список сервисов
kubectl get deployments  # Список развертываний
```

### Логи и отладка:

```bash
kubectl logs <pod-name>           # Логи пода
kubectl describe pod <pod-name>   # Детали пода
kubectl exec -it <pod-name> -- sh # Подключение к поду
```

### Масштабирование:

```bash
kubectl scale deployment chat-app --replicas=3
```

### Удаление:

```bash
kubectl delete -f deployment.yaml
kubectl delete -f service.yaml
```

## Структура проекта

- `app.py` - FastAPI приложение
- `Dockerfile` - образ контейнера
- `requirements.txt` - зависимости Python
- `deployment.yaml` - развертывание подов
- `service.yaml` - сетевой доступ

## Что изучается

1. **Контейнеризация** - упаковка приложения в Docker
2. **Deployment** - управление подами и репликами
3. **Service** - сетевой доступ к приложению
4. **Масштабирование** - увеличение количества подов
5. **Мониторинг** - просмотр логов и статуса

## Следующие шаги

После освоения базы изучите:

- ConfigMap и Secrets
- Ingress для внешнего доступа
- Persistent Volumes для данных
- Helm для управления пакетами
