### **Использование FastAPI с JSON-RPC API:**

FastAPI — это современный фреймворк для создания RESTful и GraphQL API на Python. Но можно ли его использовать для JSON-RPC API? Да, но с некоторыми оговорками.  

Рассмотрим **плюсы**, **минусы** и **альтернативы**.

---

## **1. FastAPI + JSON-RPC: Плюсы**  

### **1.1 Автоматическая документация (Swagger/OpenAPI)**  
FastAPI генерирует **Swagger-документацию** автоматически.  
Если обернуть JSON-RPC методы в FastAPI, можно получить удобное описание API.  

Пример:  
```python
from fastapi import FastAPI
from jsonrpcserver import method, async_dispatch

app = FastAPI()

@method
async def add(a: int, b: int) -> int:
    return a + b

@app.post("/rpc")
async def handle_rpc(request: dict):
    response = await async_dispatch(request)
    return response

# Теперь в Swagger (/docs) будет видно, что есть POST /rpc
```
**Плюс:**  
✅ Документация для HTTP-эндпоинта (`/rpc`).  

**Минус:**  
❌ Документация не будет показывать сами JSON-RPC методы (`add`, `get_user` и т.д.).  

---

### **1.2 Встроенная валидация данных (Pydantic)**  
FastAPI использует **Pydantic**, что позволяет валидировать входные данные.  

Пример:  
```python
from pydantic import BaseModel

class AddRequest(BaseModel):
    a: int
    b: int

@app.post("/add")
async def add_rpc(request: AddRequest):
    return {"result": request.a + request.b}
```
**Плюс:**  
✅ Валидация параметров без дополнительного кода.  

**Минус:**  
❌ Это уже не чистый JSON-RPC, а гибрид REST + JSON-RPC.  

---

### **1.3 Асинхронность (AsyncIO)**  
FastAPI поддерживает асинхронные вызовы, как и `jsonrpcserver`.  

**Плюс:**  
✅ Можно использовать `async`/`await` для высоконагруженных API.  

---

## **2. FastAPI + JSON-RPC: Минусы**  

### **2.1 Избыточность для JSON-RPC**  
FastAPI заточен под **REST/GraphQL**, а JSON-RPC — это другой стиль:  
- В REST методы определяются через **HTTP-глаголы** (`GET`, `POST`).  
- В JSON-RPC методы вызываются **внутри JSON-тела**.  

**Пример проблемы:**  
```python
@app.post("/rpc")
async def handle_rpc(request: dict):
    # FastAPI не знает, какие методы есть в JSON-RPC
    return await async_dispatch(request)
```
👉 Swagger не покажет, что можно вызывать `add` или `get_user`.  

---

### **2.2 Нет нативной поддержки JSON-RPC**  
FastAPI не имеет встроенного JSON-RPC роутера (в отличие от `jsonrpcserver`).  

**Придется:**  
- Либо писать обертку вручную.  
- Либо использовать гибридный подход (REST + JSON-RPC).  

---

### **2.3 Ограниченная польза от фич FastAPI**  
- **Dependency Injection** – бесполезен, т.к. методы вызываются через `jsonrpcserver`.  
- **Background Tasks** – сложно интегрировать.  
- **Middleware** – можно использовать, но проще в чистом JSON-RPC.  

---

## **3. Альтернативы: когда что выбрать?**  

| **Критерий**               | **Чистый JSON-RPC** (`jsonrpcserver`) | **FastAPI + JSON-RPC** | **FastAPI (REST/GraphQL)** |
|----------------------------|--------------------------------------|-----------------------|---------------------------|
| **Простота**               | ✅ Максимально просто                | ⚠️ Средняя           | ❌ Сложнее (роуты, схемы) |
| **Документация**           | ❌ Нет Swagger                       | ⚠️ Только для `/rpc`  | ✅ Полная (OpenAPI)       |
| **Валидация**              | ❌ Вручную                          | ✅ Через Pydantic     | ✅ Автоматическая         |
| **Поддержка JSON-RPC**     | ✅ Полная                           | ⚠️ Через обертку     | ❌ Нет                    |
| **Асинхронность**          | ✅ Да                               | ✅ Да                 | ✅ Да                     |
| **Использование**          | Блокчейн, IoT, RPC-сервисы          | Гибридные API         | Классические веб-API      |

---

## **4. Вывод: когда использовать FastAPI с JSON-RPC?**  

### **✅ Да, если:**  
- Нужна **документация Swagger** (даже если только для `/rpc`).  
- Хочется **гибридный API** (часть методов — REST, часть — JSON-RPC).  
- Требуется **встроенная валидация** (Pydantic).  

### **❌ Нет, если:**  
- Нужен **чистый JSON-RPC** (лучше `jsonrpcserver`).  
- API **только для внутреннего использования** (документация не важна).  
- Хочется **максимальной производительности** (минимум накладных расходов).  

### **Лучший компромисс:**  
```python
from fastapi import FastAPI
from jsonrpcserver import method, async_dispatch

app = FastAPI()

@method
async def add(a: int, b: int) -> int:
    return a + b

@app.post("/rpc")
async def handle_rpc(request: dict):
    return await async_dispatch(request)
```
👉 **FastAPI** для HTTP-обертки, **jsonrpcserver** — для обработки RPC.  

---
### **Итог**  
FastAPI можно использовать с JSON-RPC, но это **не всегда оправдано**.  
- Для **чистого JSON-RPC** лучше `jsonrpcserver`.  
- Для **REST/GraphQL** — FastAPI идеален.  
- Для **гибридных API** — можно комбинировать.  

Если вам нужен **простой и быстрый JSON-RPC API**, FastAPI может быть избыточным. 🚀