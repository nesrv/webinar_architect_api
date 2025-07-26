from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Float, Text, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
import json

app = FastAPI(title="Shop API")
engine = create_engine("sqlite:///shop.db")
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

class ProductDB(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    price = Column(Float)
    stock = Column(Integer)

class CartDB(Base):
    __tablename__ = "cart"
    id = Column(Integer, primary_key=True)
    product_id = Column(Integer)
    quantity = Column(Integer)

class OrderDB(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True)
    items = Column(Text)
    total = Column(Float)

Base.metadata.create_all(engine)

with SessionLocal() as db:
    if not db.query(ProductDB).first():
        db.add_all([
            ProductDB(id=1, name="Телефон", price=50000, stock=10),
            ProductDB(id=2, name="Ноутбук", price=80000, stock=5),
            ProductDB(id=3, name="Наушники", price=5000, stock=20)
        ])
        db.commit()

def get_db():
    with SessionLocal() as db:
        yield db

class CartItem(BaseModel):
    product_id: int
    quantity: int

@app.get("/products")
def get_products(db: Session = Depends(get_db)):
    return db.query(ProductDB).all()

@app.get("/products/{product_id}")
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(ProductDB).filter_by(id=product_id).first()
    if not product:
        raise HTTPException(404, "Товар не найден")
    return product

@app.post("/cart")
def add_to_cart(item: CartItem, db: Session = Depends(get_db)):
    product = db.query(ProductDB).filter_by(id=item.product_id).first()
    if not product or product.stock < item.quantity:
        raise HTTPException(400, "Товар недоступен")
    
    cart_item = db.query(CartDB).filter_by(product_id=item.product_id).first()
    if cart_item:
        cart_item.quantity += item.quantity
    else:
        db.add(CartDB(product_id=item.product_id, quantity=item.quantity))
    db.commit()
    return {"ok": True}

@app.get("/cart")
def get_cart(db: Session = Depends(get_db)):
    items = []
    total = 0
    for cart in db.query(CartDB).all():
        product = db.query(ProductDB).filter_by(id=cart.product_id).first()
        subtotal = product.price * cart.quantity
        items.append({"product": product.name, "quantity": cart.quantity, "subtotal": subtotal})
        total += subtotal
    return {"items": items, "total": total}

@app.post("/order")
def create_order(db: Session = Depends(get_db)):
    cart_items = db.query(CartDB).all()
    if not cart_items:
        raise HTTPException(400, "Корзина пуста")
    
    total = 0
    items = []
    for item in cart_items:
        product = db.query(ProductDB).filter_by(id=item.product_id).first()
        if product.stock < item.quantity:
            raise HTTPException(400, "Недостаточно товара")
        total += product.price * item.quantity
        items.append({"product_id": item.product_id, "quantity": item.quantity})
        product.stock -= item.quantity
    
    order = OrderDB(items=json.dumps(items), total=total)
    db.add(order)
    db.query(CartDB).delete()
    db.commit()
    return {"order_id": order.id, "total": total}

@app.get("/orders")
def get_orders(db: Session = Depends(get_db)):
    return [{"id": o.id, "items": json.loads(o.items), "total": o.total} for o in db.query(OrderDB).all()]

@app.delete("/cart/{product_id}")
def remove_from_cart(product_id: int, db: Session = Depends(get_db)):
    db.query(CartDB).filter_by(product_id=product_id).delete()
    db.commit()
    return {"ok": True}