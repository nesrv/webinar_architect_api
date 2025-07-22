# Примеры GraphQL запросов для системы управления задачами

В этом файле представлены примеры GraphQL запросов и мутаций для работы с API системы управления задачами.

## Запуск сервера

```bash
pip install fastapi uvicorn strawberry-graphql
python todo_graphql_server.py
```

После запуска сервера GraphQL Playground будет доступен по адресу: http://127.0.0.1:8000/graphql

## Запросы (Queries)

### Получение списка всех задач

```graphql
query GetAllTasks {
  tasks {
    id
    title
    description
    status
    priority
    createdAt
    tags
  }
}
```

### Получение задач с определенным статусом

```graphql
query GetTasksByStatus {
  tasks(status: "TODO") {
    id
    title
    priority
    tags
  }
}
```

### Получение детальной информации о задаче

```graphql
query GetTaskDetails {
  task(id: "задача_id") {
    id
    title
    description
    status
    priority
    createdAt
    tags
  }
}
```

### Получение списка пользователей с их задачами

```graphql
query GetUsers {
  users {
    id
    name
    email
    tasks {
      id
      title
      status
    }
  }
}
```

### Получение информации о конкретном пользователе

```graphql
query GetUserDetails {
  user(id: "пользователь_id") {
    id
    name
    email
    tasks {
      id
      title
      description
      status
      priority
      createdAt
      tags
    }
  }
}
```

## Мутации (Mutations)

### Добавление новой задачи

```graphql
mutation AddTask {
  addTask(
    userId: "пользователь_id",
    taskInput: {
      title: "Выучить GraphQL",
      description: "Изучить основы GraphQL и создать простое приложение",
      priority: 4,
      tags: ["учеба", "программирование"]
    }
  ) {
    id
    title
    status
    priority
    createdAt
    tags
  }
}
```

### Обновление статуса задачи

```graphql
mutation UpdateTaskStatus {
  updateTaskStatus(
    taskId: "задача_id",
    status: "IN_PROGRESS"
  ) {
    id
    title
    status
    priority
  }
}
```

## Сложные запросы

### Получение всех пользователей с их задачами в статусе "TODO"

```graphql
query GetUsersWithTodoTasks {
  users {
    id
    name
    email
    tasks {
      id
      title
      status
      priority
      tags
    }
  }
}
```

Примечание: Фильтрацию по статусу "TODO" можно выполнить на клиенте.

### Получение задач с высоким приоритетом

```graphql
query GetHighPriorityTasks {
  tasks {
    id
    title
    description
    status
    priority
    tags
  }
}
```

Примечание: Фильтрацию по приоритету можно выполнить на клиенте, выбрав задачи с priority >= 4.