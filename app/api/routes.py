"""
API роуты для приложения
"""
import logging
from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from typing import Dict, Any
from datetime import datetime

from app.models.schemas import (
    ProcessDataRequest, 
    ProcessDataResponse, 
    ErrorResponse, 
    HealthCheckResponse
)
from app.services.data_processor import DataProcessorService
from app.services.redis_service import RedisService
from app.config import settings

logger = logging.getLogger(__name__)

# Создаем роутер
router = APIRouter()

# Инициализируем сервисы
data_processor = DataProcessorService()
redis_service = RedisService()


@router.post("/process_data/", response_model=ProcessDataResponse)
async def process_data(request: ProcessDataRequest) -> ProcessDataResponse:
    """
    Обрабатывает входящие данные асинхронно
    
    - **data**: JSON с произвольной структурой для обработки
    
    Возвращает результат обработки с данными от внешнего API
    """
    logger.info(f"Получен запрос на обработку данных: {request.data}")
    
    try:
        # Обрабатываем данные
        result = await data_processor.process_data(request.data)
        
        logger.info(f"Обработка данных завершена, request_id: {result.request_id}")
        return result
        
    except Exception as e:
        logger.error(f"Критическая ошибка при обработке данных: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Внутренняя ошибка сервера: {str(e)}"
        )


@router.get("/health/", response_model=HealthCheckResponse)
async def health_check():
    """
    Проверка состояния сервиса
    
    Возвращает информацию о состоянии приложения и подключенных сервисов
    """
    redis_healthy = await redis_service.is_healthy()
    
    status = "healthy" if redis_healthy else "degraded"
    
    return HealthCheckResponse(
        status=status,
        app_name=settings.app_name,
        version=settings.app_version,
        timestamp=datetime.now()
    )


@router.get("/")
async def root():
    """
    Корневой эндпоинт
    
    Возвращает информацию о сервисе
    """
    return {
        "message": "Async Data Processing API",
        "version": settings.app_version,
        "docs": "/docs",
        "health": "/health/"
    }
