"""
Сервис для обработки данных
"""
import logging
import uuid
from typing import Dict, Any
from datetime import datetime
from app.models.schemas import ProcessDataResponse, ExternalApiResponse
from app.services.external_api import ExternalApiService
from app.services.redis_service import RedisService

logger = logging.getLogger(__name__)


class DataProcessorService:
    """Сервис для асинхронной обработки данных"""
    
    def __init__(self):
        self.external_api_service = ExternalApiService()
        self.redis_service = RedisService()
    
    async def process_data(self, input_data: Dict[str, Any]) -> ProcessDataResponse:
        """
        Асинхронно обрабатывает входящие данные
        
        Args:
            input_data: Входящие данные для обработки
            
        Returns:
            ProcessDataResponse: Результат обработки
        """
        request_id = str(uuid.uuid4())
        logger.info(f"Начало обработки данных, request_id: {request_id}")
        
        try:
            # Асинхронно получаем данные от внешнего API
            external_data = await self.external_api_service.get_cat_fact()
            
            # Обрабатываем входящие данные (простая трансформация)
            processed_data = self._transform_data(input_data)
            
            # Создаем ответ
            response = ProcessDataResponse(
                success=True,
                message="Данные успешно обработаны",
                processed_data=processed_data,
                external_api_data=external_data,
                timestamp=datetime.now(),
                request_id=request_id
            )
            
            # Сохраняем в Redis
            await self.redis_service.save_request(
                request_id,
                {
                    "input_data": input_data,
                    "processed_data": processed_data,
                    "external_api_data": external_data.model_dump() if external_data else None,
                    "success": True
                }
            )
            
            logger.info(f"Обработка данных завершена успешно, request_id: {request_id}")
            return response
            
        except Exception as e:
            logger.error(f"Ошибка при обработке данных, request_id: {request_id}: {str(e)}")
            
            # Сохраняем ошибку в Redis
            await self.redis_service.save_request(
                request_id,
                {
                    "input_data": input_data,
                    "error": str(e),
                    "success": False
                }
            )
            
            return ProcessDataResponse(
                success=False,
                message="Ошибка при обработке данных",
                processed_data={},
                external_api_data=None,
                timestamp=datetime.now(),
                request_id=request_id
            )
    
    def _transform_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Трансформирует входящие данные
        
        Args:
            data: Входящие данные
            
        Returns:
            Dict: Трансформированные данные
        """
        # Простая трансформация - добавляем метаданные
        transformed = {
            "original_data": data,
            "processed_at": datetime.now().isoformat(),
            "data_keys": list(data.keys()) if isinstance(data, dict) else [],
            "data_type": type(data).__name__,
            "transformation_applied": True
        }
        
        return transformed
