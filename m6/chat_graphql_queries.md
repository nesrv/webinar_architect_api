# Примеры GraphQL запросов для чата

В этом файле представлены примеры GraphQL запросов и мутаций для работы с API чата.

## Запуск сервера

```bash
pip install fastapi uvicorn strawberry-graphql
python chat_graphql_server.py
```

После запуска сервера GraphQL Playground будет доступен по адресу: http://127.0.0.1:8000/graphql

## Запросы (Queries)

### Получение списка всех чат-комнат

```graphql
query GetAllChatRooms {
  chatRooms {
    id
    name
  }
}
```

### Получение информации о конкретной чат-комнате с сообщениями

```graphql
query GetChatRoomWithMessages {
  chatRoom(id: "room-1") {
    id
    name
    messages {
      id
      content
      sender
      timestamp
    }
  }
}
```

### Получение всех сообщений

```graphql
query GetAllMessages {
  messages {
    id
    content
    sender
    timestamp
    chatRoom
  }
}
```

### Получение сообщений из конкретной чат-комнаты

```graphql
query GetMessagesFromRoom {
  messages(chatRoomId: "room-1") {
    id
    content
    sender
    timestamp
  }
}
```

## Мутации (Mutations)

### Отправка нового сообщения

```graphql
mutation SendMessage {
  sendMessage(messageInput: {
    content: "Привет! Как дела?",
    sender: "Петр",
    chatRoom: "room-1"
  }) {
    id
    content
    sender
    timestamp
    chatRoom
  }
}
```

### Создание новой чат-комнаты

```graphql
mutation CreateChatRoom {
  createChatRoom(name: "Новости") {
    id
    name
  }
}
```

## Сложные запросы

### Получение всех чат-комнат с их сообщениями

```graphql
query GetAllChatRoomsWithMessages {
  chatRooms {
    id
    name
    messages {
      id
      content
      sender
      timestamp
    }
  }
}
```

### Получение последних сообщений из всех чат-комнат

```graphql
query GetLatestMessages {
  chatRooms {
    id
    name
    messages {
      content
      sender
      timestamp
    }
  }
}
```

## Пример рабочего процесса

1. Создание новой чат-комнаты:
```graphql
mutation {
  createChatRoom(name: "Проект X") {
    id
    name
  }
}
```

2. Отправка сообщения в новую чат-комнату (используя ID, полученный на шаге 1):
```graphql
mutation {
  sendMessage(messageInput: {
    content: "Начинаем обсуждение проекта X",
    sender: "Менеджер",
    chatRoom: "room-3"  # ID из предыдущего шага
  }) {
    id
    timestamp
  }
}
```

3. Получение всех сообщений из этой чат-комнаты:
```graphql
query {
  messages(chatRoomId: "room-3") {
    content
    sender
    timestamp
  }
}
```