# Примеры GraphQL запросов для библиотечной системы

В этом файле представлены примеры GraphQL запросов и мутаций для работы с API библиотечной системы.

## Запуск сервера

```bash
pip install fastapi uvicorn strawberry-graphql
python library_graphql_server.py
```

После запуска сервера GraphQL Playground будет доступен по адресу: http://127.0.0.1:8000/graphql

## Запросы (Queries)

### Получение списка всех книг

```graphql
query GetAllBooks {
  books {
    id
    title
    genre
    publishedYear
    available
    author {
      name
    }
  }
}
```

### Получение книг определенного жанра

```graphql
query GetBooksByGenre {
  books(genre: "Роман") {
    id
    title
    publishedYear
    available
    author {
      name
    }
  }
}
```

### Получение детальной информации о книге

```graphql
query GetBookDetails {
  book(id: "книга_id") {
    id
    title
    genre
    publishedYear
    available
    author {
      id
      name
      bio
      books {
        title
      }
    }
  }
}
```

### Получение списка авторов с их книгами

```graphql
query GetAuthors {
  authors {
    id
    name
    bio
    books {
      id
      title
      publishedYear
    }
  }
}
```

### Получение информации о конкретном авторе

```graphql
query GetAuthorDetails {
  author(id: "автор_id") {
    id
    name
    bio
    books {
      id
      title
      genre
      publishedYear
      available
    }
  }
}
```

### Получение списка членов библиотеки

```graphql
query GetMembers {
  members {
    id
    name
    email
    joinedDate
    borrowedBooks {
      book {
        title
      }
      borrowDate
      dueDate
      returned
    }
  }
}
```

### Получение детальной информации о члене библиотеки

```graphql
query GetMemberDetails {
  member(id: "член_id") {
    id
    name
    email
    joinedDate
    borrowedBooks {
      id
      book {
        id
        title
        author {
          name
        }
      }
      borrowDate
      dueDate
      returned
    }
  }
}
```

## Мутации (Mutations)

### Добавление нового автора

```graphql
mutation AddAuthor {
  addAuthor(authorInput: {
    name: "Федор Достоевский",
    bio: "Русский писатель, мыслитель, философ и публицист"
  }) {
    id
    name
    bio
  }
}
```

### Добавление новой книги

```graphql
mutation AddBook {
  addBook(bookInput: {
    title: "Преступление и наказание",
    genre: "Роман",
    publishedYear: 1866,
    authorId: "автор_id"
  }) {
    id
    title
    genre
    publishedYear
    author {
      name
    }
  }
}
```

### Добавление нового члена библиотеки

```graphql
mutation AddMember {
  addMember(memberInput: {
    name: "Алексей Смирнов",
    email: "alexey@example.com"
  }) {
    id
    name
    email
    joinedDate
  }
}
```

### Заимствование книги

```graphql
mutation BorrowBook {
  borrowBook(borrowInput: {
    bookId: "книга_id",
    memberId: "член_id"
  }) {
    id
    book {
      title
    }
    member {
      name
    }
    borrowDate
    dueDate
    returned
  }
}
```

### Возврат книги

```graphql
mutation ReturnBook {
  returnBook(borrowedBookId: "заимствование_id") {
    id
    book {
      title
      available
    }
    member {
      name
    }
    borrowDate
    dueDate
    returned
  }
}
```

## Сложные запросы

### Получение всех доступных книг с информацией об авторах

```graphql
query GetAvailableBooks {
  books {
    id
    title
    genre
    publishedYear
    available
    author {
      name
      bio
      books {
        title
      }
    }
  }
}
```

### Получение информации о членах библиотеки с просроченными книгами

```graphql
query GetMembersWithOverdueBooks {
  members {
    id
    name
    email
    borrowedBooks {
      book {
        title
      }
      borrowDate
      dueDate
      returned
    }
  }
}
```

Примечание: Для проверки просроченных книг нужно будет на клиенте сравнить `dueDate` с текущей датой.