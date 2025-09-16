"""
Сервис для работы с Redis
"""
import redis.asyncio as redis
import json
import logging
from typing import Optional, Dict, Any
from datetime import datetime, timedelta
from app.config import settings

logger = logging.getLogger(__name__)


class RedisService:
    """Сервис для работы с Redis"""
    
    def __init__(self):
        self.redis_client: Optional[redis.Redis] = None
    
    async def connect(self):
        """Подключение к Redis"""
        try:
            self.redis_client = redis.Redis(
                host=settings.redis_host,
                port=settings.redis_port,
                db=settings.redis_db,
                decode_responses=True
            )
            # Проверяем подключение
            await self.redis_client.ping()
            logger.info("Успешное подключение к Redis")
        except Exception as e:
            logger.error(f"Ошибка подключения к Redis: {str(e)}")
            self.redis_client = None
    
    async def disconnect(self):
        """Отключение от Redis"""
        if self.redis_client:
            await self.redis_client.close()
            logger.info("Отключение от Redis")
    
    async def save_request(self, request_id: str, data: Dict[str, Any], ttl_hours: int = 24) -> bool:
        """
        Сохраняет данные запроса в Redis
        
        Args:
            request_id: Уникальный ID запроса
            data: Данные для сохранения
            ttl_hours: Время жизни записи в часах
            
        Returns:
            bool: True если успешно сохранено
        """
        if not self.redis_client:
            logger.warning("Redis не подключен, данные не сохранены")
            return False
        
        try:
            key = f"request:{request_id}"
            data_with_timestamp = {
                **data,
                "saved_at": datetime.now().isoformat()
            }
            
            await self.redis_client.setex(
                key,
                timedelta(hours=ttl_hours),
                json.dumps(data_with_timestamp, ensure_ascii=False)
            )
            logger.info(f"Данные запроса {request_id} сохранены в Redis")
            return True
        except Exception as e:
            logger.error(f"Ошибка сохранения в Redis: {str(e)}")
            return False
    
    async def get_request(self, request_id: str) -> Optional[Dict[str, Any]]:
        """
        Получает данные запроса из Redis
        
        Args:
            request_id: Уникальный ID запроса
            
        Returns:
            Dict с данными или None если не найдено
        """
        if not self.redis_client:
            logger.warning("Redis не подключен")
            return None
        
        try:
            key = f"request:{request_id}"
            data = await self.redis_client.get(key)
            if data:
                return json.loads(data)
            return None
        except Exception as e:
            logger.error(f"Ошибка получения данных из Redis: {str(e)}")
            return None
    
    async def is_healthy(self) -> bool:
        """Проверяет состояние Redis"""
        if not self.redis_client:
            return False
        
        try:
            await self.redis_client.ping()
            return True
        except Exception:
            return False
