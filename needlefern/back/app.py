from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import time
from typing import List, Dict, Any
from pydantic import BaseModel  # Импорт для моделей данных

app = FastAPI(title="NeedleFern DB API")

# CORS для фронтенда
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # В продакшене замените на свой домен
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --- МОДЕЛИ ДАННЫХ ДЛЯ ЗАКАЗА ---

class OrderItem(BaseModel):
    """Схема одного товара в заказе."""
    id: int
    quantity: int


class OrderData(BaseModel):
    """Схема данных, приходящих при оформлении заказа."""
    name: str
    email: str
    payment_method: str
    items: List[OrderItem]


# --- МОК/ЗАГЛУШКА БАЗЫ ДАННЫХ ---

def get_products_from_db_mock() -> List[Dict[str, Any]]:
    """
    Имитация получения данных из базы данных, включая описание.
    """
    products_data = [
        {
            "id": 1001,
            "title": "Snowman Cross Stitch and Knitting Pattern",
            "price": "3.60",
            "currency": "USD",
            "url": "https://www.etsy.com/listing/snowman-pattern-mock",
            "images": ["snowman.png"],
            "quantity": 9999,
            "description": "A charming cross stitch and knitting pattern featuring a happy snowman, perfect for winter holidays. Easy difficulty level.",
        },
        {
            "id": 1002,
            "title": "Vintage Airplane Cross Stitch Pattern",
            "price": "4.20",
            "currency": "USD",
            "url": "https://www.etsy.com/listing/airplane-pattern-mock",
            "images": ["airflot.png"],
            "quantity": 9999,
            "description": "A complex and detailed vintage airplane pattern. Suitable for experienced crafters. A wonderful gift for aviation enthusiasts.",
        },
        {
            "id": 1003,
            "title": "Christmas Bell Cross Stitch Pattern",
            "price": "3.60",
            "currency": "USD",
            "url": "https://www.etsy.com/listing/bell-pattern-mock",
            "images": ["bell.png"],
            "quantity": 50,
            "description": "A simple and elegant Christmas bell pattern. Ideal for decorating cards and small gifts.",
        },
        {
            "id": 1004,
            "title": "Cross stitch pattern Santa's Sleigh",
            "price": "3.60",
            "currency": "USD",
            "url": "https://www.etsy.com/listing/sleigh-pattern-mock",
            "images": ["moon.png"],
            "quantity": 9999,
            "description": "A cross-stitch pattern depicting Santa's sleigh. A festive design to create a holiday mood.",
        },
    ]

    # Имитация задержки БД
    time.sleep(0.5)

    return products_data


# --- ЭНДПОИНТЫ API ---

@app.get("/products")
async def get_products():
    """Получает список товаров из mock-БД."""
    try:
        products = get_products_from_db_mock()
        return {"products": products, "cached": False}

    except Exception as e:
        # В реальном приложении здесь стоит логировать ошибку
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


@app.post("/submit_order")
async def submit_order(order: OrderData):
    """
    НОВЫЙ ЭНДПОИНТ: Принимает и имитирует обработку заказа.
    """
    if not order.items:
        raise HTTPException(status_code=400, detail="Cart is empty.")

    # --- ИМИТАЦИЯ БИЗНЕС-ЛОГИКИ ---

    # 1. Проверка доступности (в реальном приложении)
    # product_check = check_stock(order.items)
    # if not product_check: ...

    # 2. Сохранение заказа в БД (в реальном приложении)
    order_id = int(time.time() * 1000)

    # 3. Имитация инициации платежа
    time.sleep(1)

    # 4. Логирование и ответ
    print("\n--- НОВЫЙ ЗАКАЗ ПОЛУЧЕН ---")
    print(f"ID Заказа: {order_id}")
    print(f"Клиент: {order.name}, Email: {order.email}")
    print(f"Метод оплаты: {order.payment_method}")
    print(f"Количество позиций: {len(order.items)}")
    print("--------------------------\n")

    return {
        "message": "Order successfully processed and payment initiated.",
        "order_id": order_id,
        "total_items": len(order.items)
    }


if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)