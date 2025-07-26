## Разберем **Kubernetes (K8s)** шаг за шагом, с упором на практику. 
Мы будем использовать **FastAPI, PostgreSQL и RabbitMQ**, чтобы закрепить знания на реальном примере.  

---

## **1. Основы Kubernetes: Краткий ликбез**
### **1.1 Что такое Kubernetes?**
Kubernetes — это система для **оркестрации контейнеров**, которая автоматизирует:
- Развертывание (**Deployment**)
- Масштабирование (**Scaling**)
- Управление (**Management**)  
контейнеризированных приложений.

### **1.2 Основные концепции**
| Термин             | Описание                                                                 |
|--------------------|-------------------------------------------------------------------------|
| **Pod**            | Минимальная единица в K8s (1+ контейнеров, общий сетевой namespace).   |
| **Deployment**     | Описывает, как развертывать и обновлять Pod'ы.                         |
| **Service**        | Постоянный IP для доступа к Pod'ам (даже если Pod'ы перезапускаются).  |
| **Ingress**        | Маршрутизация HTTP/HTTPS трафика в Service.                            |
| **ConfigMap**      | Хранение конфигураций (например, env-переменные).                      |
| **Secret**         | Хранение чувствительных данных (пароли, токены).                       |
| **PersistentVolume (PV)** | Диск для хранения данных (чтобы они не терялись при перезапуске Pod'а). |
| **StatefulSet**    | Управление Pod'ами с состоянием (например, базы данных).               |

---

## **2. Установка и настройка Kubernetes**
### **2.1 Локальная разработка (Minikube / Kind)**
Для начала установите **Minikube** (локальный K8s-кластер) или **Kind** (Kubernetes in Docker):
```bash
# Установка Minikube (требуется Docker)
minikube start --driver=docker
minikube status
```

### **2.2 kubectl — CLI для управления K8s**
Установите `kubectl` — основную утилиту для работы с Kubernetes:
```bash
kubectl get nodes  # Проверить ноды
kubectl get pods   # Посмотреть Pod'ы
```

---

## **3. Развертывание FastAPI + PostgreSQL + RabbitMQ в Kubernetes**
### **3.1 FastAPI (Stateless-сервис)**
Создаем **Deployment** и **Service** для FastAPI:
```yaml
# fastapi-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: fastapi-app
spec:
  replicas: 2
  selector:
    matchLabels:
      app: fastapi
  template:
    metadata:
      labels:
        app: fastapi
    spec:
      containers:
      - name: fastapi
        image: ваш-образ-fastapi:latest
        ports:
        - containerPort: 8000
        env:
        - name: DATABASE_URL
          value: "postgresql://user:password@postgres-service:5432/db"
        - name: RABBITMQ_URL
          value: "amqp://user:password@rabbitmq-service:5672/"
---
# fastapi-service.yaml
apiVersion: v1
kind: Service
metadata:
  name: fastapi-service
spec:
  selector:
    app: fastapi
  ports:
    - protocol: TCP
      port: 80
      targetPort: 8000
```

### **3.2 PostgreSQL (StatefulSet + PersistentVolume)**
```yaml
# postgres-statefulset.yaml
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: postgres
spec:
  serviceName: postgres-service
  replicas: 1
  selector:
    matchLabels:
      app: postgres
  template:
    metadata:
      labels:
        app: postgres
    spec:
      containers:
      - name: postgres
        image: postgres:13
        env:
        - name: POSTGRES_USER
          value: "user"
        - name: POSTGRES_PASSWORD
          value: "password"
        - name: POSTGRES_DB
          value: "db"
        ports:
        - containerPort: 5432
        volumeMounts:
        - name: postgres-storage
          mountPath: /var/lib/postgresql/data
  volumeClaimTemplates:
  - metadata:
      name: postgres-storage
    spec:
      accessModes: [ "ReadWriteOnce" ]
      resources:
        requests:
          storage: 1Gi
---
# postgres-service.yaml
apiVersion: v1
kind: Service
metadata:
  name: postgres-service
spec:
  selector:
    app: postgres
  ports:
    - port: 5432
      targetPort: 5432
```

### **3.3 RabbitMQ (Deployment + Service)**
```yaml
# rabbitmq-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: rabbitmq
spec:
  replicas: 1
  selector:
    matchLabels:
      app: rabbitmq
  template:
    metadata:
      labels:
        app: rabbitmq
    spec:
      containers:
      - name: rabbitmq
        image: rabbitmq:3-management
        ports:
        - containerPort: 5672
        - containerPort: 15672
        env:
        - name: RABBITMQ_DEFAULT_USER
          value: "user"
        - name: RABBITMQ_DEFAULT_PASS
          value: "password"
---
# rabbitmq-service.yaml
apiVersion: v1
kind: Service
metadata:
  name: rabbitmq-service
spec:
  selector:
    app: rabbitmq
  ports:
    - name: amqp
      port: 5672
      targetPort: 5672
    - name: management
      port: 15672
      targetPort: 15672
```

### **3.4 Применяем конфигурации**
```bash
kubectl apply -f fastapi-deployment.yaml
kubectl apply -f fastapi-service.yaml
kubectl apply -f postgres-statefulset.yaml
kubectl apply -f rabbitmq-deployment.yaml
```

---

## **4. Доступ к сервисам**
### **4.1 Port Forwarding (локальный доступ)**
```bash
kubectl port-forward svc/fastapi-service 8000:80
kubectl port-forward svc/rabbitmq-service 15672:15672  # RabbitMQ Management UI
```
Теперь FastAPI доступен на `http://localhost:8000`, а RabbitMQ — `http://localhost:15672`.

### **4.2 Ingress (если нужен внешний доступ)**
```yaml
# ingress.yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: fastapi-ingress
spec:
  rules:
  - host: fastapi.local
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: fastapi-service
            port:
              number: 80
```
Применяем:
```bash
kubectl apply -f ingress.yaml
```
Добавляем в `/etc/hosts`:
```
127.0.0.1 fastapi.local
```

---

## **5. Масштабирование и обновления**
### **5.1 Horizontal Pod Autoscaler (HPA)**
```bash
kubectl autoscale deployment fastapi-app --cpu-percent=50 --min=2 --max=5
```

### **5.2 Rolling Update**
```bash
kubectl set image deployment/fastapi-app fastapi=новый-образ:версия
```

---

## **6. Мониторинг и логи**
### **6.1 Prometheus + Grafana**
```bash
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm install prometheus prometheus-community/kube-prometheus-stack
```

### **6.2 Логи (Loki + Grafana)**
```bash
helm repo add grafana https://grafana.github.io/helm-charts
helm install loki grafana/loki-stack
```

---

## **7. Что дальше?**
1. **Helm** — для управления чартами (пакетами K8s).
2. **CI/CD** — автоматический деплой (GitHub Actions / ArgoCD).
3. **Service Mesh** (Istio / Linkerd) — для трафика между сервисами.
4. **Kustomize** — для управления конфигами.

---

### **Итог**
Теперь у вас есть:
- FastAPI в Kubernetes (с масштабированием).
- PostgreSQL с Persistent Volume.
- RabbitMQ для асинхронных задач.
- Доступ через Ingress / Port Forwarding.
