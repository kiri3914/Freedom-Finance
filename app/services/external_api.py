"""
Сервис для работы с внешними API
"""
import httpx
import logging
from typing import Optional
from app.config import settings
from app.models.schemas import ExternalApiResponse

logger = logging.getLogger(__name__)


class ExternalApiService:
    """Сервис для взаимодействия с внешними API"""
    
    def __init__(self):
        self.base_url = settings.external_api_url
        self.timeout = settings.external_api_timeout
    
    async def get_cat_fact(self) -> Optional[ExternalApiResponse]:
        """
        Получает случайный факт о кошках от catfact.ninja API
        
        Returns:
            ExternalApiResponse или None в случае ошибки
        """
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                logger.info(f"Запрос к внешнему API: {self.base_url}")
                response = await client.get(self.base_url)
                response.raise_for_status()
                
                data = response.json()
                logger.info(f"Получен ответ от внешнего API: {data}")
                
                return ExternalApiResponse(
                    fact=data.get("fact", ""),
                    length=data.get("length", 0)
                )
                
        except httpx.TimeoutException:
            logger.error(f"Таймаут при запросе к внешнему API: {self.base_url}")
            return None
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP ошибка при запросе к внешнему API: {e.response.status_code}")
            return None
        except Exception as e:
            logger.error(f"Неожиданная ошибка при запросе к внешнему API: {str(e)}")
            return None
