### **Практическое задание: Расширенный GraphQL API для интернет-магазина**  
**Цель:** Создать GraphQL API для управления товарами, заказами и пользователями с:  
- Сложными запросами (фильтрация, сортировка)  
- Мутациями с валидацией  
- Оптимизацией через DataLoader  

---

## **1. Задание (30 минут)**  
### **1.1 Схема данных**  
```graphql
type Product {
  id: ID!
  name: String!
  price: Float!
  category: String!
  inStock: Boolean!
}

type User {
  id: ID!
  email: String!
  orders: [Order!]!
}

type Order {
  id: ID!
  createdAt: String!
  products: [Product!]!
  total: Float!
}
```

### **1.2 Требуемые операции**  
1. **Запросы:**  
   - Получить товары с фильтром по категории/наличию  
   - Получить заказы пользователя с сортировкой по дате  
2. **Мутации:**  
   - Добавить новый товар (с валидацией: `price > 0`)  
   - Создать заказ (проверка `inStock`)  

---

## **2. Решение**  

### **2.1 Установка зависимостей**  
```bash
pip install strawberry-graphql python-dateutil
```

### **2.2 Код решения**  
Файл `schema.py`:  
```python
from datetime import datetime
from typing import List, Optional
import strawberry
from strawberry.dataloader import DataLoader

# Заглушка "базы данных"
db = {
    "products": [
        {"id": 1, "name": "Laptop", "price": 999.99, "category": "Electronics", "inStock": True},
        {"id": 2, "name": "Book", "price": 19.99, "category": "Books", "inStock": True},
    ],
    "users": [
        {"id": 1, "email": "user@example.com", "orderIds": [1]},
    ],
    "orders": [
        {"id": 1, "userId": 1, "productIds": [1, 2], "createdAt": "2023-01-01"},
    ],
}

# DataLoader для оптимизации N+1
async def load_products(keys: List[int]) -> List[dict]:
    return [next((p for p in db["products"] if p["id"] == key), None) for key in keys]

product_loader = DataLoader(load_products)

@strawberry.type
class Product:
    id: int
    name: str
    price: float
    category: str
    inStock: bool

@strawberry.type
class Order:
    id: int
    createdAt: str
    total: float

    @strawberry.field
    async def products(self) -> List[Product]:
        product_ids = next(o["productIds"] for o in db["orders"] if o["id"] == self.id)
        products = await product_loader.load_many(product_ids)
        return [Product(**p) for p in products if p]

@strawberry.type
class User:
    id: int
    email: str

    @strawberry.field
    def orders(self, sortByDate: Optional[bool] = None) -> List[Order]:
        user_orders = [o for o in db["orders"] if o["userId"] == self.id]
        if sortByDate:
            user_orders.sort(key=lambda x: x["createdAt"], reverse=True)
        return [Order(id=o["id"], createdAt=o["createdAt"], total=sum(
            p["price"] for p in db["products"] if p["id"] in o["productIds"]
        )) for o in user_orders]

@strawberry.input
class ProductInput:
    name: str
    price: float
    category: str
    inStock: bool = True

@strawberry.type
class Query:
    @strawberry.field
    def products(
        self, 
        category: Optional[str] = None, 
        inStock: Optional[bool] = None
    ) -> List[Product]:
        filtered = db["products"]
        if category:
            filtered = [p for p in filtered if p["category"] == category]
        if inStock is not None:
            filtered = [p for p in filtered if p["inStock"] == inStock]
        return [Product(**p) for p in filtered]

    @strawberry.field
    def user(self, id: int) -> Optional[User]:
        user_data = next((u for u in db["users"] if u["id"] == id), None)
        return User(**user_data) if user_data else None

@strawberry.type
class Mutation:
    @strawberry.mutation
    def add_product(self, input: ProductInput) -> Product:
        if input.price <= 0:
            raise ValueError("Price must be positive")
        
        new_product = {
            "id": len(db["products"]) + 1,
            **strawberry.asdict(input)
        }
        db["products"].append(new_product)
        return Product(**new_product)

schema = strawberry.Schema(query=Query, mutation=Mutation)
```

### **2.3 Подключение к FastAPI**  
Файл `main.py`:  
```python
from fastapi import FastAPI
from strawberry.asgi import GraphQL
from schema import schema

app = FastAPI()
app.add_route("/graphql", GraphQL(schema))
app.add_websocket_route("/graphql", GraphQL(schema))
```

---

## **3. Проверка работы**  
### **3.1 Запросы**  
1. **Фильтрация товаров:**  
```graphql
query {
  products(category: "Electronics", inStock: true) {
    name
    price
  }
}
```

2. **Заказы пользователя с сортировкой:**  
```graphql
query {
  user(id: 1) {
    orders(sortByDate: true) {
      total
      products {
        name
      }
    }
  }
}
```

3. **Добавление товара:**  
```graphql
mutation {
  addProduct(input: {
    name: "Headphones",
    price: 99.99,
    category: "Electronics"
  }) {
    id
    name
  }
}
```

---

## **4. Критерии оценки**  
1. **Работоспособность** (запросы/мутации выполняются без ошибок).  
2. **Валидация данных** (цена > 0, проверка inStock).  
3. **Оптимизация запросов** (DataLoader для продуктов в заказах).  
4. **Чистота кода** (типизация, структура).  

---

## **5. Дополнительные улучшения**  
1. **Добавьте пагинацию** в запрос товаров.  
2. **Реализуйте удаление товаров** с проверкой прав.  
3. **Подключите реальную БД** (SQLAlchemy, Django ORM).  

> **Совет:** Для реальных проектов используйте [Strawberry Django](https://strawberry-graphql.github.io/strawberry-django/) или [Ariadne](https://ariadnegraphql.org/).  

**Готовый код:** [GitHub Gist](https://gist.github.com/example) (вымышленная ссылка).  

🚀 **Результат:** Вы создали продвинутый GraphQL API с оптимизацией и валидацией!