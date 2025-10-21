import logging
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from schemas import ProductResponse, ProductCreate
from models import Product
from database import get_session


app = FastAPI(title="Shop API", description="API для Telegram-магазина", version="1.0")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@app.get("/products", response_model=list[ProductResponse])
async def get_products(session: AsyncSession = Depends(get_session)):
    logger.info("Запрос /products")
    result = await session.execute(select(Product))
    return result.scalars().all()


@app.get("/product/{product_id}", response_model=ProductResponse)
async def get_product(product_id: int, session: AsyncSession = Depends(get_session)):
    product = await session.get(Product, product_id)
    if not product:
        logger.warning(f"Товар {product_id} не найден")
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@app.post("/products", status_code=201, response_model=ProductResponse)
async def add_product(product: ProductCreate, session: AsyncSession = Depends(get_session)):
    db_product = Product(**product.dict())
    session.add(db_product)
    await session.commit()
    await session.refresh(db_product)
    return db_product


@app.put("/product/{product_id}", response_model=ProductResponse)
async def update_product(product_id: int, updated: ProductCreate, session: AsyncSession = Depends(get_session)):
    existing = await session.get(Product, product_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Product not found")
    existing.name = updated.name
    existing.price = updated.price
    existing.description = updated.description
    existing.category = updated.category
    await session.commit()
    await session.refresh(existing)
    return existing


@app.delete("/product/{product_id}")
async def delete_product(product_id: int, session: AsyncSession = Depends(get_session)):
    product = await session.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    await session.delete(product)
    await session.commit()
    return {"detail": "Deleted"}
