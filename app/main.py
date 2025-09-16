"""
Основной файл FastAPI приложения
"""
import logging
import sys
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import uuid

from app.config import settings
from app.api.routes import router
from app.services.redis_service import RedisService
from app.models.schemas import ErrorResponse

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("app.log")
    ]
)

logger = logging.getLogger(__name__)

# Глобальный экземпляр Redis сервиса
redis_service = RedisService()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Управление жизненным циклом приложения
    """
    # Startup
    logger.info("Запуск приложения...")
    await redis_service.connect()
    logger.info("Приложение запущено успешно")
    
    yield
    
    # Shutdown
    logger.info("Остановка приложения...")
    await redis_service.disconnect()
    logger.info("Приложение остановлено")


# Создание FastAPI приложения
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Асинхронный REST API-сервис обработки данных",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc"
)

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Middleware для логирования запросов
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Логирование всех HTTP запросов"""
    request_id = str(uuid.uuid4())
    start_time = datetime.now()
    
    # Логируем входящий запрос
    logger.info(
        f"Входящий запрос {request_id}: {request.method} {request.url.path} "
        f"от {request.client.host if request.client else 'unknown'}"
    )
    
    # Обрабатываем запрос
    response = await call_next(request)
    
    # Логируем ответ
    process_time = (datetime.now() - start_time).total_seconds()
    logger.info(
        f"Ответ {request_id}: {response.status_code} "
        f"за {process_time:.3f}с"
    )
    
    # Добавляем request_id в заголовки ответа
    response.headers["X-Request-ID"] = request_id
    
    return response


# Обработчики исключений
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Обработчик HTTP исключений"""
    request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
    
    logger.error(f"HTTP ошибка {request_id}: {exc.status_code} - {exc.detail}")
    
    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponse(
            error=f"HTTP {exc.status_code}",
            detail=exc.detail,
            timestamp=datetime.now(),
            request_id=request_id
        ).dict()
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Обработчик общих исключений"""
    request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
    
    logger.error(f"Неожиданная ошибка {request_id}: {str(exc)}", exc_info=True)
    
    return JSONResponse(
        status_code=500,
        content=ErrorResponse(
            error="Internal Server Error",
            detail="Произошла внутренняя ошибка сервера",
            timestamp=datetime.now(),
            request_id=request_id
        ).dict()
    )


# Подключение роутов
app.include_router(router, prefix="/api/v1")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
        log_level="info"
    )
