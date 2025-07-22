from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter
import strawberry
import typing
import uuid
from datetime import datetime, timedelta

# Модели данных
@strawberry.type
class Author:
    id: str
    name: str
    bio: str
    books: typing.List["Book"]

@strawberry.type
class Book:
    id: str
    title: str
    genre: str
    published_year: int
    available: bool
    author: Author

@strawberry.type
class Member:
    id: str
    name: str
    email: str
    joined_date: str
    borrowed_books: typing.List["BorrowedBook"]

@strawberry.type
class BorrowedBook:
    id: str
    book: Book
    member: Member
    borrow_date: str
    due_date: str
    returned: bool

# Входные типы для мутаций
@strawberry.input
class AuthorInput:
    name: str
    bio: str

@strawberry.input
class BookInput:
    title: str
    genre: str
    published_year: int
    author_id: str

@strawberry.input
class MemberInput:
    name: str
    email: str

@strawberry.input
class BorrowBookInput:
    book_id: str
    member_id: str

# База данных (имитация)
authors_db = {}
books_db = {}
members_db = {}
borrowed_books_db = {}

# Заполняем базу данными для примера
def initialize_db():
    # Авторы
    author1_id = str(uuid.uuid4())
    author2_id = str(uuid.uuid4())
    
    authors_db[author1_id] = {
        "id": author1_id,
        "name": "Лев Толстой",
        "bio": "Русский писатель, классик мировой литературы",
        "books": []
    }
    
    authors_db[author2_id] = {
        "id": author2_id,
        "name": "Джордж Оруэлл",
        "bio": "Английский писатель и публицист",
        "books": []
    }
    
    # Книги
    book1_id = str(uuid.uuid4())
    book2_id = str(uuid.uuid4())
    book3_id = str(uuid.uuid4())
    
    books_db[book1_id] = {
        "id": book1_id,
        "title": "Война и мир",
        "genre": "Роман",
        "published_year": 1869,
        "available": True,
        "author_id": author1_id
    }
    
    books_db[book2_id] = {
        "id": book2_id,
        "title": "Анна Каренина",
        "genre": "Роман",
        "published_year": 1877,
        "available": True,
        "author_id": author1_id
    }
    
    books_db[book3_id] = {
        "id": book3_id,
        "title": "1984",
        "genre": "Антиутопия",
        "published_year": 1949,
        "available": True,
        "author_id": author2_id
    }
    
    # Добавляем книги к авторам
    authors_db[author1_id]["books"].append(book1_id)
    authors_db[author1_id]["books"].append(book2_id)
    authors_db[author2_id]["books"].append(book3_id)
    
    # Члены библиотеки
    member1_id = str(uuid.uuid4())
    member2_id = str(uuid.uuid4())
    
    members_db[member1_id] = {
        "id": member1_id,
        "name": "Иван Иванов",
        "email": "ivan@example.com",
        "joined_date": datetime.now().strftime("%Y-%m-%d"),
        "borrowed_books": []
    }
    
    members_db[member2_id] = {
        "id": member2_id,
        "name": "Мария Петрова",
        "email": "maria@example.com",
        "joined_date": datetime.now().strftime("%Y-%m-%d"),
        "borrowed_books": []
    }

# Инициализируем базу данных
initialize_db()

# Резолверы для типов
def get_author_for_book(book: Book) -> Author:
    author_data = authors_db[books_db[book.id]["author_id"]]
    author_books = []
    for book_id in author_data["books"]:
        book_data = books_db[book_id]
        author_books.append(Book(
            id=book_id,
            title=book_data["title"],
            genre=book_data["genre"],
            published_year=book_data["published_year"],
            available=book_data["available"],
            author=None  # Избегаем циклической зависимости
        ))
    
    return Author(
        id=author_data["id"],
        name=author_data["name"],
        bio=author_data["bio"],
        books=author_books
    )

def get_books_for_author(author: Author) -> typing.List[Book]:
    books = []
    for book_id in authors_db[author.id]["books"]:
        book_data = books_db[book_id]
        books.append(Book(
            id=book_id,
            title=book_data["title"],
            genre=book_data["genre"],
            published_year=book_data["published_year"],
            available=book_data["available"],
            author=None  # Избегаем циклической зависимости
        ))
    return books

def get_borrowed_books_for_member(member: Member) -> typing.List[BorrowedBook]:
    borrowed_books = []
    for borrowed_id in members_db[member.id]["borrowed_books"]:
        borrowed_data = borrowed_books_db[borrowed_id]
        book_data = books_db[borrowed_data["book_id"]]
        
        book = Book(
            id=book_data["id"],
            title=book_data["title"],
            genre=book_data["genre"],
            published_year=book_data["published_year"],
            available=book_data["available"],
            author=get_author_for_book(Book(id=book_data["id"], title="", genre="", published_year=0, available=True, author=None))
        )
        
        member_data = members_db[borrowed_data["member_id"]]
        member_obj = Member(
            id=member_data["id"],
            name=member_data["name"],
            email=member_data["email"],
            joined_date=member_data["joined_date"],
            borrowed_books=[]  # Избегаем циклической зависимости
        )
        
        borrowed_books.append(BorrowedBook(
            id=borrowed_id,
            book=book,
            member=member_obj,
            borrow_date=borrowed_data["borrow_date"],
            due_date=borrowed_data["due_date"],
            returned=borrowed_data["returned"]
        ))
    
    return borrowed_books

# Определение запросов
@strawberry.type
class Query:
    @strawberry.field
    def book(self, id: str) -> typing.Optional[Book]:
        if id not in books_db:
            return None
        
        book_data = books_db[id]
        return Book(
            id=book_data["id"],
            title=book_data["title"],
            genre=book_data["genre"],
            published_year=book_data["published_year"],
            available=book_data["available"],
            author=get_author_for_book(Book(id=book_data["id"], title="", genre="", published_year=0, available=True, author=None))
        )
    
    @strawberry.field
    def books(self, genre: typing.Optional[str] = None) -> typing.List[Book]:
        result = []
        for book_id, book_data in books_db.items():
            if genre is None or book_data["genre"] == genre:
                result.append(Book(
                    id=book_data["id"],
                    title=book_data["title"],
                    genre=book_data["genre"],
                    published_year=book_data["published_year"],
                    available=book_data["available"],
                    author=get_author_for_book(Book(id=book_data["id"], title="", genre="", published_year=0, available=True, author=None))
                ))
        return result
    
    @strawberry.field
    def author(self, id: str) -> typing.Optional[Author]:
        if id not in authors_db:
            return None
        
        author_data = authors_db[id]
        return Author(
            id=author_data["id"],
            name=author_data["name"],
            bio=author_data["bio"],
            books=get_books_for_author(Author(id=author_data["id"], name="", bio="", books=[]))
        )
    
    @strawberry.field
    def authors(self) -> typing.List[Author]:
        result = []
        for author_id, author_data in authors_db.items():
            result.append(Author(
                id=author_data["id"],
                name=author_data["name"],
                bio=author_data["bio"],
                books=get_books_for_author(Author(id=author_data["id"], name="", bio="", books=[]))
            ))
        return result
    
    @strawberry.field
    def member(self, id: str) -> typing.Optional[Member]:
        if id not in members_db:
            return None
        
        member_data = members_db[id]
        member = Member(
            id=member_data["id"],
            name=member_data["name"],
            email=member_data["email"],
            joined_date=member_data["joined_date"],
            borrowed_books=[]
        )
        
        member.borrowed_books = get_borrowed_books_for_member(member)
        return member
    
    @strawberry.field
    def members(self) -> typing.List[Member]:
        result = []
        for member_id, member_data in members_db.items():
            member = Member(
                id=member_data["id"],
                name=member_data["name"],
                email=member_data["email"],
                joined_date=member_data["joined_date"],
                borrowed_books=[]
            )
            
            member.borrowed_books = get_borrowed_books_for_member(member)
            result.append(member)
        
        return result

# Определение мутаций
@strawberry.type
class Mutation:
    @strawberry.mutation
    def add_author(self, author_input: AuthorInput) -> Author:
        author_id = str(uuid.uuid4())
        authors_db[author_id] = {
            "id": author_id,
            "name": author_input.name,
            "bio": author_input.bio,
            "books": []
        }
        
        return Author(
            id=author_id,
            name=author_input.name,
            bio=author_input.bio,
            books=[]
        )
    
    @strawberry.mutation
    def add_book(self, book_input: BookInput) -> typing.Optional[Book]:
        if book_input.author_id not in authors_db:
            return None
        
        book_id = str(uuid.uuid4())
        books_db[book_id] = {
            "id": book_id,
            "title": book_input.title,
            "genre": book_input.genre,
            "published_year": book_input.published_year,
            "available": True,
            "author_id": book_input.author_id
        }
        
        # Добавляем книгу к автору
        authors_db[book_input.author_id]["books"].append(book_id)
        
        return Book(
            id=book_id,
            title=book_input.title,
            genre=book_input.genre,
            published_year=book_input.published_year,
            available=True,
            author=get_author_for_book(Book(id=book_id, title="", genre="", published_year=0, available=True, author=None))
        )
    
    @strawberry.mutation
    def add_member(self, member_input: MemberInput) -> Member:
        member_id = str(uuid.uuid4())
        members_db[member_id] = {
            "id": member_id,
            "name": member_input.name,
            "email": member_input.email,
            "joined_date": datetime.now().strftime("%Y-%m-%d"),
            "borrowed_books": []
        }
        
        return Member(
            id=member_id,
            name=member_input.name,
            email=member_input.email,
            joined_date=datetime.now().strftime("%Y-%m-%d"),
            borrowed_books=[]
        )
    
    @strawberry.mutation
    def borrow_book(self, borrow_input: BorrowBookInput) -> typing.Optional[BorrowedBook]:
        if borrow_input.book_id not in books_db or borrow_input.member_id not in members_db:
            return None
        
        book_data = books_db[borrow_input.book_id]
        
        # Проверяем, доступна ли книга
        if not book_data["available"]:
            return None
        
        # Отмечаем книгу как недоступную
        books_db[borrow_input.book_id]["available"] = False
        
        # Создаем запись о заимствовании
        borrow_id = str(uuid.uuid4())
        borrow_date = datetime.now()
        due_date = borrow_date + timedelta(days=14)  # 2 недели на чтение
        
        borrowed_books_db[borrow_id] = {
            "id": borrow_id,
            "book_id": borrow_input.book_id,
            "member_id": borrow_input.member_id,
            "borrow_date": borrow_date.strftime("%Y-%m-%d"),
            "due_date": due_date.strftime("%Y-%m-%d"),
            "returned": False
        }
        
        # Добавляем запись к читателю
        members_db[borrow_input.member_id]["borrowed_books"].append(borrow_id)
        
        book = Book(
            id=book_data["id"],
            title=book_data["title"],
            genre=book_data["genre"],
            published_year=book_data["published_year"],
            available=False,
            author=get_author_for_book(Book(id=book_data["id"], title="", genre="", published_year=0, available=True, author=None))
        )
        
        member_data = members_db[borrow_input.member_id]
        member = Member(
            id=member_data["id"],
            name=member_data["name"],
            email=member_data["email"],
            joined_date=member_data["joined_date"],
            borrowed_books=[]
        )
        
        return BorrowedBook(
            id=borrow_id,
            book=book,
            member=member,
            borrow_date=borrow_date.strftime("%Y-%m-%d"),
            due_date=due_date.strftime("%Y-%m-%d"),
            returned=False
        )
    
    @strawberry.mutation
    def return_book(self, borrowed_book_id: str) -> typing.Optional[BorrowedBook]:
        if borrowed_book_id not in borrowed_books_db:
            return None
        
        borrowed_data = borrowed_books_db[borrowed_book_id]
        
        # Проверяем, не возвращена ли уже книга
        if borrowed_data["returned"]:
            return None
        
        # Отмечаем книгу как возвращенную
        borrowed_books_db[borrowed_book_id]["returned"] = True
        
        # Делаем книгу снова доступной
        books_db[borrowed_data["book_id"]]["available"] = True
        
        book_data = books_db[borrowed_data["book_id"]]
        book = Book(
            id=book_data["id"],
            title=book_data["title"],
            genre=book_data["genre"],
            published_year=book_data["published_year"],
            available=True,
            author=get_author_for_book(Book(id=book_data["id"], title="", genre="", published_year=0, available=True, author=None))
        )
        
        member_data = members_db[borrowed_data["member_id"]]
        member = Member(
            id=member_data["id"],
            name=member_data["name"],
            email=member_data["email"],
            joined_date=member_data["joined_date"],
            borrowed_books=[]
        )
        
        return BorrowedBook(
            id=borrowed_book_id,
            book=book,
            member=member,
            borrow_date=borrowed_data["borrow_date"],
            due_date=borrowed_data["due_date"],
            returned=True
        )

# Создаем схему GraphQL
schema = strawberry.Schema(query=Query, mutation=Mutation)

# Создаем FastAPI приложение
app = FastAPI()

# Добавляем GraphQL маршрут
graphql_app = GraphQLRouter(schema)
app.include_router(graphql_app, prefix="/graphql")

# Добавляем корневой маршрут с информацией
@app.get("/")
def read_root():
    return {
        "message": "Библиотечная система с GraphQL API",
        "graphql_endpoint": "/graphql",
        "graphql_playground": "/graphql"
    }

# Запуск сервера
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)