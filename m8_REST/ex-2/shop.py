from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI(title="Интернет-магазин", description="Простой REST API для интернет-магазина", version="1.0.0")

class Product(BaseModel):
    id: int
    name: str
    price: float
    stock: int

class CartItem(BaseModel):
    product_id: int
    quantity: int

class Order(BaseModel):
    id: int
    items: List[CartItem]
    total: float

products = [
    Product(id=1, name="Телефон", price=50000, stock=10),
    Product(id=2, name="Ноутбук", price=80000, stock=5),
    Product(id=3, name="Наушники", price=5000, stock=20)
]

cart = []
orders = []
order_counter = 1

@app.get("/products", summary="Получить все товары")
def get_products():
    return products

@app.get("/products/{product_id}", summary="Получить товар по ID")
def get_product(product_id: int):
    product = next((p for p in products if p.id == product_id), None)
    if not product:
        raise HTTPException(status_code=404, detail="Товар не найден")
    return product

@app.post("/cart", summary="Добавить товар в корзину")
def add_to_cart(item: CartItem):
    product = next((p for p in products if p.id == item.product_id), None)
    if not product or product.stock < item.quantity:
        raise HTTPException(status_code=400, detail="Товар недоступен")
    
    existing = next((c for c in cart if c.product_id == item.product_id), None)
    if existing:
        existing.quantity += item.quantity
    else:
        cart.append(item)
    return {"message": "Добавлено в корзину"}

@app.get("/cart", summary="Просмотр корзины")
def get_cart():
    cart_details = []
    total = 0
    for item in cart:
        product = next(p for p in products if p.id == item.product_id)
        subtotal = product.price * item.quantity
        cart_details.append({
            "product": product.name,
            "price": product.price,
            "quantity": item.quantity,
            "subtotal": subtotal
        })
        total += subtotal
    return {"items": cart_details, "total": total}

@app.post("/order", summary="Создать заказ")
def create_order():
    global order_counter
    if not cart:
        raise HTTPException(status_code=400, detail="Корзина пуста")
    
    total = 0
    for item in cart:
        product = next(p for p in products if p.id == item.product_id)
        if product.stock < item.quantity:
            raise HTTPException(status_code=400, detail="Недостаточно товара")
        total += product.price * item.quantity
        product.stock -= item.quantity
    
    order = Order(id=order_counter, items=cart.copy(), total=total)
    orders.append(order)
    cart.clear()
    order_counter += 1
    return {"order_id": order.id, "total": total}

@app.get("/orders", summary="Получить все заказы")
def get_orders():
    return orders

@app.delete("/cart/{product_id}", summary="Удалить товар из корзины")
def remove_from_cart(product_id: int):
    global cart
    cart = [item for item in cart if item.product_id != product_id]
    return {"message": "Удалено из корзины"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)