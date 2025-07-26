from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import redis
import json

app = FastAPI(title="Shop Redis API")
r = redis.Redis(host='localhost', port=6379, decode_responses=True)

# Инициализация данных
if not r.exists("products"):
    products = {
        "1": {"name": "Телефон", "price": 50000, "stock": 10},
        "2": {"name": "Ноутбук", "price": 80000, "stock": 5},
        "3": {"name": "Наушники", "price": 5000, "stock": 20}
    }
    r.hset("products", mapping={k: json.dumps(v) for k, v in products.items()})

class CartItem(BaseModel):
    product_id: int
    quantity: int

@app.get("/products")
def get_products():
    products = r.hgetall("products")
    return [{"id": int(k), **json.loads(v)} for k, v in products.items()]

@app.get("/products/{product_id}")
def get_product(product_id: int):
    product = r.hget("products", str(product_id))
    if not product:
        raise HTTPException(404, "Товар не найден")
    return {"id": product_id, **json.loads(product)}

@app.post("/cart")
def add_to_cart(item: CartItem):
    product = r.hget("products", str(item.product_id))
    if not product:
        raise HTTPException(404, "Товар не найден")
    
    product_data = json.loads(product)
    if product_data["stock"] < item.quantity:
        raise HTTPException(400, "Недостаточно товара")
    
    current = r.hget("cart", str(item.product_id))
    quantity = item.quantity + (int(current) if current else 0)
    r.hset("cart", str(item.product_id), quantity)
    return {"ok": True}

@app.get("/cart")
def get_cart():
    cart = r.hgetall("cart")
    items = []
    total = 0
    
    for product_id, quantity in cart.items():
        product = json.loads(r.hget("products", product_id))
        subtotal = product["price"] * int(quantity)
        items.append({
            "product": product["name"],
            "quantity": int(quantity),
            "subtotal": subtotal
        })
        total += subtotal
    
    return {"items": items, "total": total}

@app.post("/order")
def create_order():
    cart = r.hgetall("cart")
    if not cart:
        raise HTTPException(400, "Корзина пуста")
    
    total = 0
    items = []
    
    for product_id, quantity in cart.items():
        product_data = json.loads(r.hget("products", product_id))
        qty = int(quantity)
        
        if product_data["stock"] < qty:
            raise HTTPException(400, "Недостаточно товара")
        
        total += product_data["price"] * qty
        items.append({"product_id": int(product_id), "quantity": qty})
        
        # Обновляем остаток
        product_data["stock"] -= qty
        r.hset("products", product_id, json.dumps(product_data))
    
    # Создаем заказ
    order_id = r.incr("order_counter")
    order = {"id": order_id, "items": items, "total": total}
    r.hset("orders", str(order_id), json.dumps(order))
    
    # Очищаем корзину
    r.delete("cart")
    
    return {"order_id": order_id, "total": total}

@app.get("/orders")
def get_orders():
    orders = r.hgetall("orders")
    return [json.loads(order) for order in orders.values()]

@app.delete("/cart/{product_id}")
def remove_from_cart(product_id: int):
    r.hdel("cart", str(product_id))
    return {"ok": True}