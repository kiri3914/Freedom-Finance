# 🚀 Асинхронный REST API-сервис обработки данных

**Техническое задание от Freedom Finance**

Микросервис на FastAPI для асинхронной обработки HTTP-запросов с интеграцией внешних API и Redis для хранения истории запросов.

## 📋 Техническое задание

### Цель проекта
Разработать микросервис, обрабатывающий асинхронные HTTP-запросы и взаимодействующий с внешними API. Сервис должен быть контейнеризирован с помощью Docker.

### Функциональные требования
- **POST /process_data/** - Принимает JSON с произвольной структурой
- Выполняет асинхронную обработку данных
- Делает асинхронный HTTP-запрос к внешнему публичному API (catfact.ninja)
- Возвращает результат обработки с данными от внешнего API

### Технологические требования
- **Язык:** Python 3.11+
- **Фреймворк:** FastAPI
- **Асинхронность:** async/await, httpx
- **Докеризация:** Dockerfile + docker-compose.yml
- **Контейнеризация:** возможность запуска через 1 команду

### Дополнительные функции (реализованы)
- ✅ Логирование всех запросов и ответов
- ✅ Обработка исключений и ошибок
- ✅ Redis для хранения истории запросов
- ✅ Unit тесты (pytest)
- ✅ Конфигурация через Pydantic BaseSettings
- ✅ Swagger документация

## 🚀 Функциональность

### API Эндпоинты
- **POST /api/v1/process_data/** - Асинхронная обработка произвольных JSON данных
- **GET /api/v1/health/** - Проверка состояния сервиса и подключенных сервисов
- **GET /api/v1/** - Информация о сервисе
- **GET /docs** - Swagger UI документация
- **GET /redoc** - ReDoc документация

### Интеграции
- **Внешний API:** catfact.ninja (получение фактов о кошках)
- **Redis:** хранение истории запросов и ответов
- **Логирование:** подробные логи всех операций

## 🛠 Технологический стек

- **Python 3.11+** - основной язык программирования
- **FastAPI** - современный веб-фреймворк для API
- **httpx** - асинхронный HTTP клиент
- **Redis** - кэширование и хранение данных
- **Pydantic** - валидация данных и настройки
- **Docker** - контейнеризация
- **pytest** - тестирование
- **uvicorn** - ASGI сервер

## 📁 Структура проекта

```
tech_task_freedom/
├── app/
│   ├── __init__.py
│   ├── main.py                 # Основной файл приложения
│   ├── config.py               # Конфигурация через Pydantic
│   ├── api/
│   │   ├── __init__.py
│   │   └── routes.py           # API роуты
│   ├── services/
│   │   ├── __init__.py
│   │   ├── external_api.py     # Сервис внешнего API
│   │   ├── redis_service.py    # Сервис Redis
│   │   └── data_processor.py   # Обработчик данных
│   └── models/
│       ├── __init__.py
│       └── schemas.py          # Pydantic модели
├── tests/
│   ├── __init__.py
│   ├── test_api.py             # Тесты API
│   └── test_services.py        # Тесты сервисов
├── requirements.txt            # Python зависимости
├── Dockerfile                  # Docker образ
├── docker-compose.yml          # Docker Compose
├── pytest.ini                 # Настройки pytest
├── .gitignore                 # Git ignore файл
└── README.md                  # Документация
```

## 🚀 Быстрый старт

### Способ 1: Docker Compose (рекомендуется)

**Один командой запустить весь стек:**

```bash
# Клонируйте репозиторий
git clone https://github.com/kiri3914/Freedom-Finance
cd tech_task_freedom

# Запустите все сервисы одной командой
docker-compose up --build
```

**Что происходит:**
- Собирается Docker образ приложения
- Запускается Redis контейнер
- Запускается FastAPI приложение
- Все сервисы подключаются друг к другу

**Сервис будет доступен по адресу:**
- 🌐 **API:** http://localhost:8000
- 📚 **Swagger UI:** http://localhost:8000/docs
- 📖 **ReDoc:** http://localhost:8000/redoc
- ❤️ **Health Check:** http://localhost:8000/api/v1/health/

### Способ 2: Локальная разработка

**Для разработки и отладки:**

```bash
# 1. Создайте виртуальное окружение
python -m venv venv

# 2. Активируйте окружение
# Linux/Mac:
source venv/bin/activate
# Windows:
venv\Scripts\activate

# 3. Установите зависимости
pip install -r requirements.txt

# 4. Запустите Redis (в отдельном терминале)
docker run -d -p 6379:6379 --name redis_dev redis:7-alpine

# 5. Запустите приложение
python -m app.main
```

### Способ 3: Только Docker (без docker-compose)

```bash
# 1. Соберите образ
docker build -t async-data-api .

# 2. Запустите Redis
docker run -d -p 6379:6379 --name redis redis:7-alpine

# 3. Запустите приложение
docker run -p 8000:8000 --link redis:redis async-data-api
```

## 📖 API Документация

### 🔥 POST /api/v1/process_data/

**Основной эндпоинт для обработки данных**

Обрабатывает входящие данные асинхронно и интегрируется с внешним API.

**Запрос:**
```bash
curl -X POST http://localhost:8000/api/v1/process_data/ \
  -H "Content-Type: application/json" \
  -d '{
    "data": {
      "user_id": 12345,
      "action": "process_payment",
      "amount": 100.50,
      "metadata": {
        "currency": "USD",
        "description": "Payment processing"
      }
    }
  }'
```

**Ответ (успешный):**
```json
{
  "success": true,
  "message": "Данные успешно обработаны",
  "processed_data": {
    "original_data": {
      "user_id": 12345,
      "action": "process_payment",
      "amount": 100.50,
      "metadata": {
        "currency": "USD",
        "description": "Payment processing"
      }
    },
    "processed_at": "2025-09-16T15:19:27.976088",
    "data_keys": ["user_id", "action", "amount", "metadata"],
    "data_type": "dict",
    "transformation_applied": true
  },
  "external_api_data": {
    "fact": "Cats can rotate their ears 180 degrees.",
    "length": 42
  },
  "timestamp": "2025-09-16T15:19:27.976096",
  "request_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
}
```

**Ответ (ошибка):**
```json
{
  "success": false,
  "error": "HTTP 422",
  "detail": "Field required",
  "timestamp": "2025-09-16T15:19:27.976096",
  "request_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
}
```

### ❤️ GET /api/v1/health/

**Проверка состояния сервиса**

Проверяет состояние приложения и подключенных сервисов (Redis).

**Запрос:**
```bash
curl -X GET http://localhost:8000/api/v1/health/
```

**Ответ (здоровый):**
```json
{
  "status": "healthy",
  "app_name": "Async Data Processing API",
  "version": "1.0.0",
  "timestamp": "2025-09-16T15:19:27.976096"
}
```

**Ответ (деградированный - Redis недоступен):**
```json
{
  "status": "degraded",
  "app_name": "Async Data Processing API",
  "version": "1.0.0",
  "timestamp": "2025-09-16T15:19:27.976096"
}
```

### ℹ️ GET /api/v1/

**Информация о сервисе**

Возвращает базовую информацию о сервисе.

**Запрос:**
```bash
curl -X GET http://localhost:8000/api/v1/
```

**Ответ:**
```json
{
  "message": "Async Data Processing API",
  "version": "1.0.0",
  "docs": "/docs",
  "health": "/health/"
}
```

### 📚 Swagger UI

**Интерактивная документация API**

- **URL:** http://localhost:8000/docs
- **Описание:** Полная интерактивная документация с возможностью тестирования API
- **Функции:** 
  - Просмотр всех эндпоинтов
  - Тестирование запросов прямо в браузере
  - Схемы данных и валидация
  - Примеры запросов и ответов

### 📖 ReDoc

**Альтернативная документация**

- **URL:** http://localhost:8000/redoc
- **Описание:** Красивая документация в стиле ReDoc

## 🧪 Тестирование

### Запуск тестов

**Все тесты:**
```bash
# Локально
pytest

# С подробным выводом
pytest -v

# С покрытием кода
pytest --cov=app
```

**Конкретные тесты:**
```bash
# Только API тесты
pytest tests/test_api.py -v

# Только тесты сервисов
pytest tests/test_services.py -v

# Конкретный тест
pytest tests/test_api.py::TestProcessDataEndpoint::test_process_data_success -v
```

**В Docker:**
```bash
# Запуск тестов в контейнере
docker-compose exec app pytest

# Или в отдельном контейнере
docker run --rm -v $(pwd):/app -w /app python:3.11-slim bash -c "pip install -r requirements.txt && pytest"
```

### Результаты тестирования

**✅ Все тесты проходят:**
- **20 unit тестов** - 100% успешно
- **API тесты** - 8 тестов
- **Сервисы тесты** - 12 тестов
- **Покрытие** - все основные компоненты

**Пример вывода:**
```
=========================================== test session starts ===========================================
platform darwin -- Python 3.9.21, pytest-7.4.3, pluggy-1.6.0
collected 20 items

tests/test_api.py::TestProcessDataEndpoint::test_process_data_success PASSED                        [  5%]
tests/test_api.py::TestProcessDataEndpoint::test_process_data_external_api_failure PASSED           [ 10%]
tests/test_api.py::TestProcessDataEndpoint::test_process_data_invalid_input PASSED                  [ 15%]
tests/test_api.py::TestHealthCheckEndpoint::test_health_check_healthy PASSED                        [ 20%]
tests/test_api.py::TestHealthCheckEndpoint::test_health_check_degraded PASSED                       [ 25%]
tests/test_api.py::TestRootEndpoint::test_root_endpoint PASSED                                      [ 30%]
tests/test_api.py::TestErrorHandling::test_404_error PASSED                                         [ 35%]
tests/test_api.py::TestErrorHandling::test_method_not_allowed PASSED                                [ 40%]
tests/test_services.py::TestExternalApiService::test_get_cat_fact_success PASSED                    [ 45%]
tests/test_services.py::TestExternalApiService::test_get_cat_fact_timeout PASSED                    [ 50%]
tests/test_services.py::TestExternalApiService::test_get_cat_fact_http_error PASSED                 [ 55%]
tests/test_services.py::TestRedisService::test_connect_success PASSED                               [ 60%]
tests/test_services.py::TestRedisService::test_save_request_success PASSED                          [ 65%]
tests/test_services.py::TestRedisService::test_save_request_no_connection PASSED                    [ 70%]
tests/test_services.py::TestRedisService::test_get_request_success PASSED                           [ 75%]
tests/test_services.py::TestRedisService::test_is_healthy_true PASSED                               [ 80%]
tests/test_services.py::TestRedisService::test_is_healthy_false PASSED                              [ 85%]
tests/test_services.py::TestDataProcessorService::test_process_data_success PASSED                  [ 90%]
tests/test_services.py::TestDataProcessorService::test_process_data_external_api_failure PASSED     [ 95%]
tests/test_services.py::TestDataProcessorService::test_transform_data PASSED                        [100%]

=========================================== 20 passed in 0.37s ===========================================
```

## ⚙️ Конфигурация

### Переменные окружения

Настройки приложения можно изменить через переменные окружения:

```bash
# Основные настройки приложения
APP_NAME=Async Data Processing API
APP_VERSION=1.0.0
DEBUG=True

# Настройки сервера
HOST=0.0.0.0
PORT=8000

# Redis настройки
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0

# Внешний API настройки
EXTERNAL_API_URL=https://catfact.ninja/fact
EXTERNAL_API_TIMEOUT=10
```

### Файл .env

Создайте файл `.env` в корне проекта:

```bash
# Скопируйте пример конфигурации
cp .env.example .env

# Отредактируйте настройки
nano .env
```

### Docker Compose переменные

В `docker-compose.yml` можно переопределить переменные:

```yaml
environment:
  - REDIS_HOST=redis
  - REDIS_PORT=6379
  - DEBUG=False
  - EXTERNAL_API_TIMEOUT=15
```

## 📊 Логирование

### Что логируется

Приложение ведет подробные логи всех операций:

- **HTTP запросы и ответы** - каждый запрос с request_id
- **Обработка данных** - этапы обработки входящих данных
- **Интеграция с внешними API** - запросы к catfact.ninja
- **Redis операции** - подключение, сохранение, получение данных
- **Ошибки и исключения** - детальная информация об ошибках
- **Производительность** - время выполнения запросов

### Формат логов

```
2025-09-16 15:19:27,976 - app.main - INFO - Входящий запрос a1b2c3d4: POST /api/v1/process_data/ от 127.0.0.1
2025-09-16 15:19:27,980 - app.services.external_api - INFO - Запрос к внешнему API: https://catfact.ninja/fact
2025-09-16 15:19:28,100 - app.services.external_api - INFO - Получен ответ от внешнего API: {"fact": "Cats can...", "length": 42}
2025-09-16 15:19:28,105 - app.services.redis_service - INFO - Данные запроса a1b2c3d4 сохранены в Redis
2025-09-16 15:19:28,110 - app.main - INFO - Ответ a1b2c3d4: 200 за 0.134с
```

### Где найти логи

- **Консоль** - выводятся в реальном времени
- **Файл** - `app.log` в корне проекта
- **Docker** - `docker-compose logs app`

### Уровни логирования

- **INFO** - обычные операции
- **ERROR** - ошибки и исключения
- **WARNING** - предупреждения (например, Redis недоступен)

## 🐳 Docker

### Docker Compose (рекомендуется)

**Запуск всего стека:**
```bash
# Запуск всех сервисов
docker-compose up

# Запуск в фоне
docker-compose up -d

# Пересборка и запуск
docker-compose up --build

# Остановка
docker-compose down

# Остановка с удалением volumes
docker-compose down -v
```

**Просмотр логов:**
```bash
# Все сервисы
docker-compose logs

# Только приложение
docker-compose logs app

# Следить за логами в реальном времени
docker-compose logs -f app
```

**Выполнение команд в контейнере:**
```bash
# Запуск тестов
docker-compose exec app pytest

# Подключение к контейнеру
docker-compose exec app bash

# Проверка Redis
docker-compose exec redis redis-cli ping
```

### Отдельные Docker команды

**Сборка образа:**
```bash
docker build -t async-data-api .
```

**Запуск приложения:**
```bash
# С Redis
docker run -d --name redis redis:7-alpine
docker run -p 8000:8000 --link redis:redis async-data-api

# Без Redis (режим деградации)
docker run -p 8000:8000 async-data-api
```

**Проверка контейнеров:**
```bash
# Список контейнеров
docker ps

# Логи контейнера
docker logs async-api_app

# Остановка
docker stop async-api_app async-api_redis
```

## ✅ Проверка работы

### Быстрая проверка

**1. Запустите сервис:**
```bash
docker-compose up --build
```

**2. Проверьте health check:**
```bash
curl http://localhost:8000/api/v1/health/
# Ожидаемый ответ: {"status":"healthy",...}
```

**3. Протестируйте основной эндпоинт:**
```bash
curl -X POST http://localhost:8000/api/v1/process_data/ \
  -H "Content-Type: application/json" \
  -d '{"data": {"test": "value"}}'
# Ожидаемый ответ: {"success":true,...}
```

**4. Откройте Swagger UI:**
- Перейдите в браузер: http://localhost:8000/docs
- Протестируйте API через интерфейс

### Полная проверка

**1. Запуск тестов:**
```bash
# Локально
pytest -v

# В Docker
docker-compose exec app pytest -v
```

**2. Проверка логов:**
```bash
# Просмотр логов
docker-compose logs app

# Следить за логами
docker-compose logs -f app
```

**3. Проверка Redis:**
```bash
# Подключение к Redis
docker-compose exec redis redis-cli

# В Redis CLI:
> KEYS *
> GET request:*
```

### Примеры использования

**Обработка платежных данных:**
```bash
curl -X POST http://localhost:8000/api/v1/process_data/ \
  -H "Content-Type: application/json" \
  -d '{
    "data": {
      "payment_id": "pay_123456",
      "amount": 99.99,
      "currency": "USD",
      "user_id": 12345,
      "metadata": {
        "source": "mobile_app",
        "timestamp": "2025-09-16T15:30:00Z"
      }
    }
  }'
```

**Обработка пользовательских данных:**
```bash
curl -X POST http://localhost:8000/api/v1/process_data/ \
  -H "Content-Type: application/json" \
  -d '{
    "data": {
      "user": {
        "id": 12345,
        "name": "John Doe",
        "email": "john@example.com"
      },
      "action": "profile_update",
      "changes": ["name", "email"]
    }
  }'
```

**Обработка JSON массивов:**
```bash
curl -X POST http://localhost:8000/api/v1/process_data/ \
  -H "Content-Type: application/json" \
  -d '{
    "data": {
      "items": [1, 2, 3, 4, 5],
      "operation": "sum",
      "result": null
    }
  }'
```

## 🔧 Разработка

### Структура кода

- **app/main.py** - точка входа приложения с настройкой FastAPI
- **app/config.py** - конфигурация через Pydantic BaseSettings
- **app/api/routes.py** - API эндпоинты
- **app/services/** - бизнес-логика и интеграции
- **app/models/schemas.py** - Pydantic модели для валидации

### Добавление новых эндпоинтов

1. Добавьте модель в `app/models/schemas.py`
2. Создайте роут в `app/api/routes.py`
3. Добавьте тесты в `tests/test_api.py`

### Добавление новых сервисов

1. Создайте файл в `app/services/`
2. Реализуйте асинхронные методы
3. Добавьте тесты в `tests/test_services.py`

## 🎯 Соответствие техническому заданию

### ✅ Выполненные требования

**Основные функции:**
- ✅ POST /process_data/ - принимает JSON с произвольной структурой
- ✅ Асинхронная обработка данных
- ✅ HTTP-запрос к внешнему API (catfact.ninja)
- ✅ Возврат результата с данными от внешнего API

**Технические требования:**
- ✅ Python 3.11+ (совместимый с 3.9+)
- ✅ FastAPI фреймворк
- ✅ Асинхронность (async/await, httpx)
- ✅ Docker контейнеризация
- ✅ Запуск одной командой (docker-compose up)

**Дополнительные функции:**
- ✅ Логирование всех запросов и ответов
- ✅ Обработка исключений и ошибок
- ✅ Redis для хранения истории
- ✅ Unit тесты (20 тестов, 100% проходят)
- ✅ Pydantic BaseSettings для конфигурации
- ✅ Swagger документация

### 📊 Статистика проекта

- **Строк кода:** ~800
- **Файлов:** 15
- **Тестов:** 20 (100% проходят)
- **Эндпоинтов:** 3 основных + документация
- **Сервисов:** 3 (API, Redis, Data Processor)
- **Моделей данных:** 5

### 🏗 Архитектурные решения

**1. Модульная архитектура:**
- Четкое разделение ответственности
- Легкое тестирование и поддержка
- Возможность расширения

**2. Асинхронность:**
- Все операции выполняются асинхронно
- Высокая производительность
- Эффективное использование ресурсов

**3. Обработка ошибок:**
- Graceful degradation при недоступности Redis
- Детальное логирование ошибок
- Понятные сообщения об ошибках

**4. Конфигурируемость:**
- Все настройки через переменные окружения
- Поддержка .env файлов
- Гибкая настройка для разных сред

## 🚀 Быстрый старт для Freedom Finance

**1. Клонирование и запуск:**
```bash
git clone <repository-url>
cd tech_task_freedom
docker-compose up --build
```

**2. Проверка работы:**
```bash
# Health check
curl http://localhost:8000/api/v1/health/

# Тест основного эндпоинта
curl -X POST http://localhost:8000/api/v1/process_data/ \
  -H "Content-Type: application/json" \
  -d '{"data": {"test": "freedom_finance"}}'
```

**3. Документация:**
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 📝 Лицензия

MIT License

## 🤝 Вклад в проект

1. Форкните репозиторий
2. Создайте ветку для новой функции
3. Внесите изменения
4. Добавьте тесты
5. Создайте Pull Request

## 📞 Поддержка

При возникновении проблем:
1. Проверьте логи приложения
2. Убедитесь, что Redis запущен
3. Проверьте доступность внешнего API
4. Создайте Issue в репозитории

---

**Проект выполнен в соответствии с техническим заданием Freedom Finance** 🎯
