# E-commerce Service

Репозиторий содержит FastAPI backend, Telegram-бот и MySQL базу данных для простого e-commerce сервиса. Все компоненты запускаются через Docker Compose.

---

## Структура проекта
```
ecommerce_service/
├─ api/ # FastAPI backend
│ ├─ main.py
│ ├─ models.py
│ ├─ database.py
│ ├─ schemas.py
│ ├─ Dockerfile
│ └─ requirements.txt
├─ bot/ # Telegram-бот
│ ├─ main.py
│ ├─ .env      -->  Настройте `.env` для бота
│ ├─ Dockerfile
│ └─ requirements.txt
├─ db/ # Инициализация базы данных
│ └─ init.sql
├─ docker-compose.yml
└─ README.md
```
---

## Требования

- Установленный Docker и Docker Compose
- Токен Telegram-бота
- MySQL (только если запуск без Docker, опционально)

---

## Настройка
### Клонируем репозиторий
- git clone <URL_репозитория>

cd ecommerce_service

### 1. Настройка `.env` для бота

В файле `bot/.env`:

```dotenv```
BOT_TOKEN=токен_вашего_бота
API_URL=http://fastapi_service:8000
ADMIN_IDS=ваш_telegram_id

Замените значения на реальные токен бота и ID администратора(ов) в Telegram.

### 2. Запуск через Docker Compose

В корневой директории проекта:

- docker compose up --build -d

Будут запущены:

MySQL на порту 3308
FastAPI на порту 8000
Telegram-бот (подключается к FastAPI)
Adminer на порту 8080 (веб-интерфейс для работы с базой)

База данных автоматически 
создается и заполняется начальными товарами из db/init.sql.

### 3. Доступ к сервисам

FastAPI: http://localhost:8000
Adminer: http://localhost:8080 (логин с учетными данными из docker-compose.yml)
Telegram-бот: через ваш Telegram аккаунт с токеном бота

#### Примечания

Бот взаимодействует с FastAPI через API_URL в .env.
Администраторы задаются в .env через ADMIN_IDS.
Таблицы базы данных создаются автоматически и наполняются начальными товарами из init.sql.
Если Docker недоступен, проект можно запустить локально, но потребуется вручную установить Python-зависимости и MySQL.

### Команды Docker

Сборка контейнеров: docker compose build
Запуск сервисов: docker compose up
Остановка сервисов: docker compose down
Просмотр логов: docker compose logs -f
