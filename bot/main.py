import os
import random

import aiohttp
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from dotenv import load_dotenv
import asyncio

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
API_URL = os.getenv("API_URL")
ADMIN_IDS = [int(x) for x in os.getenv("ADMIN_IDS", "").split(",") if x.strip()]

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


def main_menu():
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Список товаров", callback_data="list"),
                InlineKeyboardButton(text="Поиск товара", callback_data="search")
            ],
            [
                InlineKeyboardButton(text="Категория", callback_data="category"),
                InlineKeyboardButton(text="Случайный товар", callback_data="random")
            ],
            [
                InlineKeyboardButton(text="Статистика", callback_data="stats")
            ]
        ]
    )
    return kb


@dp.message(Command("start"))
async def start_cmd(msg: types.Message):
    await msg.answer("Привет! Я бот-магазин.")
    await msg.answer("Используй /list чтобы увидеть товары.")
    if msg.from_user.id in ADMIN_IDS:
        await msg.answer("Ты админ! Используй /help чтобы увидеть все команды и примеры.")


@dp.message(Command("help"))
async def help_cmd(msg: types.Message):
    user_id = msg.from_user.id
    base_commands = (
        "/start - запустить бота\n"
        "/list - показать главное меню\n"
        "/search <слово> - поиск товара\n"
        "/category <название> - товары по категории\n"
        "/help - эта подсказка"
    )

    admin_commands = (
        "\n\nАДМИН КОМАНДЫ:\n"
        "/add_product <name>;<price>;<description>;<category> - добавить товар\n"
        "   Пример: /add_product Ноутбук;299000;Мощный ноутбук;Ноутбуки\n"
        "/update_product <id>;<name>;<price>;<description>;<category> - обновить товар\n"
        "   Пример: /update_product 2;Ноутбук Pro;350000;Обновленный ноутбук;Ноутбуки\n"
        "/delete_product <id> - удалить товар\n"
        "   Пример: /delete_product 2"
    )

    text = base_commands
    if user_id in ADMIN_IDS:
        text += admin_commands

    await msg.answer(text)


@dp.message(Command("list"))
async def list_cmd(msg: types.Message):
    await msg.answer("Главное меню:", reply_markup=main_menu())


@dp.callback_query()
async def callbacks(cb: types.CallbackQuery):
    action = cb.data

    async with aiohttp.ClientSession() as session:
        async with session.get(f"{API_URL}/products") as resp:
            data = await resp.json()

    if action == "list":
        if not data:
            await cb.message.answer("Пока нет товаров.")
            return
        text = "\n".join([f"{p['id']}. {p['name']} — {p['price']}₸ - category: {p['category']}" for p in data])
        await cb.message.answer(text)

    elif action == "random":
        if not data:
            await cb.message.answer("Пока нет товаров.")
            return
        p = random.choice(data)
        text = f"{p['id']}. {p['name']} — {p['price']}₸\n{p.get('description', '')}"
        await cb.message.answer(text)

    elif action == "stats":
        if not data:
            await cb.message.answer("Товары пока отсутствуют")
            return
        total = len(data)
        avg_price = sum(p['price'] for p in data) / total
        await cb.message.answer(f"Всего товаров: {total}\nСредняя цена: {avg_price:.2f}₸")

    elif action in ("search", "category"):
        await cb.message.answer("Для этой функции пока нужно написать текст вручную:\n"
                                "/search <слово> или /category <название>")


@dp.message(Command("search"))
async def search_cmd(msg: types.Message):
    try:
        query = msg.text.split(maxsplit=1)[1].lower()
    except IndexError:
        await msg.answer("Используй: /search <слово>")
        return

    async with aiohttp.ClientSession() as session:
        async with session.get(f"{API_URL}/products") as resp:
            data = await resp.json()

    results = [p for p in data if query in p['name'].lower() or query in p['description'].lower()]
    if not results:
        await msg.answer("Ничего не найдено")
        return
    text = "\n".join([f"{p['id']}. {p['name']} — {p['price']}₸" for p in results])
    await msg.answer(text)


@dp.message(Command("category"))
async def category_cmd(msg: types.Message):
    try:
        category = msg.text.split(maxsplit=1)[1].lower()
    except IndexError:
        await msg.answer("Используй: /category <название>")
        return

    async with aiohttp.ClientSession() as session:
        async with session.get(f"{API_URL}/products") as resp:
            data = await resp.json()

    results = [p for p in data if p.get('category', '').lower() == category]
    if not results:
        await msg.answer("Товаров в этой категории нет")
        return
    text = "\n".join([f"{p['id']}. {p['name']} — {p['price']}₸" for p in results])
    await msg.answer(text)


@dp.message(Command("add_product"))
async def add_product_cmd(msg: types.Message):
    if msg.from_user.id not in ADMIN_IDS:
        await msg.answer("У тебя нет доступа 😕")
        return

    try:
        # Пример формата: /add_product Ноутбук;299000;Мощный ноутбук;Ноутбуки
        _, content = msg.text.split(maxsplit=1)
        name, price, description, category = map(str.strip, content.split(";"))
        price = float(price)
    except Exception:
        await msg.answer("Используй: /add_product <name>;<price>;<description>;<category>")
        return

    async with aiohttp.ClientSession() as session:
        async with session.post(f"{API_URL}/products", json={
            "name": name,
            "price": price,
            "description": description,
            "category": category
        }) as resp:
            if resp.status == 201:
                await msg.answer("Товар успешно добавлен ✅")
            else:
                await msg.answer(f"Ошибка добавления: {resp.status}")


@dp.message(Command("update_product"))
async def update_product_cmd(msg: types.Message):
    if msg.from_user.id not in ADMIN_IDS:
        await msg.answer("У тебя нет доступа 😕")
        return

    try:
        # Пример: /update_product 2;Ноутбук Pro;350000;Обновленный ноутбук;Ноутбуки
        _, content = msg.text.split(maxsplit=1)
        product_id_str, name, price, description, category = map(str.strip, content.split(";"))
        product_id = int(product_id_str)
        price = float(price)
    except Exception:
        await msg.answer("Используй: /update_product <id>;<name>;<price>;<description>;<category>")
        return

    async with aiohttp.ClientSession() as session:
        async with session.put(f"{API_URL}/product/{product_id}", json={
            "name": name,
            "price": price,
            "description": description,
            "category": category
        }) as resp:
            if resp.status == 200:
                await msg.answer("Товар успешно обновлён ✅")
            elif resp.status == 404:
                await msg.answer("Товар не найден")
            else:
                await msg.answer(f"Ошибка обновления: {resp.status}")


@dp.message(Command("delete_product"))
async def delete_product_cmd(msg: types.Message):
    if msg.from_user.id not in ADMIN_IDS:
        await msg.answer("У тебя нет доступа 😕")
        return

    try:
        product_id = int(msg.text.split()[1])
    except (IndexError, ValueError):
        await msg.answer("Используй: /delete_product <id>")
        return

    async with aiohttp.ClientSession() as session:
        async with session.delete(f"{API_URL}/product/{product_id}") as resp:
            if resp.status == 200:
                await msg.answer("Товар удалён ✅")
            elif resp.status == 404:
                await msg.answer("Товар не найден")
            else:
                await msg.answer(f"Ошибка удаления: {resp.status}")


async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
