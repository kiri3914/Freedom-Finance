"""
Unit тесты для сервисов
"""
import pytest
import httpx
from unittest.mock import AsyncMock, patch
from datetime import datetime

from app.services.external_api import ExternalApiService
from app.services.redis_service import RedisService
from app.services.data_processor import DataProcessorService
from app.models.schemas import ExternalApiResponse


class TestExternalApiService:
    """Тесты для ExternalApiService"""
    
    @pytest.mark.asyncio
    async def test_get_cat_fact_success(self):
        """Тест успешного получения факта о кошке"""
        service = ExternalApiService()
        
        mock_response = ExternalApiResponse(
            fact="Cats can rotate their ears 180 degrees.",
            length=42
        )
        
        with patch.object(service, 'get_cat_fact', return_value=mock_response):
            result = await service.get_cat_fact()
            
            assert result is not None
            assert isinstance(result, ExternalApiResponse)
            assert result.fact == "Cats can rotate their ears 180 degrees."
            assert result.length == 42
    
    @pytest.mark.asyncio
    async def test_get_cat_fact_timeout(self):
        """Тест таймаута при запросе к внешнему API"""
        service = ExternalApiService()
        
        with patch.object(service, 'get_cat_fact', return_value=None):
            result = await service.get_cat_fact()
            
            assert result is None
    
    @pytest.mark.asyncio
    async def test_get_cat_fact_http_error(self):
        """Тест HTTP ошибки при запросе к внешнему API"""
        service = ExternalApiService()
        
        with patch.object(service, 'get_cat_fact', return_value=None):
            result = await service.get_cat_fact()
            
            assert result is None


class TestRedisService:
    """Тесты для RedisService"""
    
    @pytest.mark.asyncio
    async def test_connect_success(self):
        """Тест успешного подключения к Redis"""
        service = RedisService()
        
        with patch('redis.asyncio.Redis') as mock_redis_class:
            mock_redis = AsyncMock()
            mock_redis.ping.return_value = True
            mock_redis_class.return_value = mock_redis
            
            await service.connect()
            
            assert service.redis_client is not None
    
    @pytest.mark.asyncio
    async def test_save_request_success(self):
        """Тест успешного сохранения запроса"""
        service = RedisService()
        service.redis_client = AsyncMock()
        service.redis_client.setex = AsyncMock(return_value=True)
        
        test_data = {"test": "data"}
        result = await service.save_request("test_id", test_data)
        
        assert result is True
        service.redis_client.setex.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_save_request_no_connection(self):
        """Тест сохранения запроса без подключения к Redis"""
        service = RedisService()
        service.redis_client = None
        
        test_data = {"test": "data"}
        result = await service.save_request("test_id", test_data)
        
        assert result is False
    
    @pytest.mark.asyncio
    async def test_get_request_success(self):
        """Тест успешного получения запроса"""
        service = RedisService()
        service.redis_client = AsyncMock()
        service.redis_client.get = AsyncMock(return_value='{"test": "data"}')
        
        result = await service.get_request("test_id")
        
        assert result == {"test": "data"}
    
    @pytest.mark.asyncio
    async def test_is_healthy_true(self):
        """Тест проверки здоровья Redis при подключении"""
        service = RedisService()
        service.redis_client = AsyncMock()
        service.redis_client.ping = AsyncMock(return_value=True)
        
        result = await service.is_healthy()
        
        assert result is True
    
    @pytest.mark.asyncio
    async def test_is_healthy_false(self):
        """Тест проверки здоровья Redis при отсутствии подключения"""
        service = RedisService()
        service.redis_client = None
        
        result = await service.is_healthy()
        
        assert result is False


class TestDataProcessorService:
    """Тесты для DataProcessorService"""
    
    @pytest.mark.asyncio
    async def test_process_data_success(self):
        """Тест успешной обработки данных"""
        service = DataProcessorService()
        
        mock_external_response = ExternalApiResponse(
            fact="Test fact",
            length=10
        )
        
        with patch.object(service.external_api_service, 'get_cat_fact') as mock_get_fact, \
             patch.object(service.redis_service, 'save_request') as mock_save:
            
            mock_get_fact.return_value = mock_external_response
            mock_save.return_value = True
            
            test_data = {"test_key": "test_value"}
            result = await service.process_data(test_data)
            
            assert result.success is True
            assert result.message == "Данные успешно обработаны"
            assert result.external_api_data == mock_external_response
            assert "original_data" in result.processed_data
            assert result.processed_data["original_data"] == test_data
            assert result.request_id is not None
    
    @pytest.mark.asyncio
    async def test_process_data_external_api_failure(self):
        """Тест обработки данных при недоступности внешнего API"""
        service = DataProcessorService()
        
        with patch.object(service.external_api_service, 'get_cat_fact') as mock_get_fact, \
             patch.object(service.redis_service, 'save_request') as mock_save:
            
            mock_get_fact.return_value = None
            mock_save.return_value = True
            
            test_data = {"test_key": "test_value"}
            result = await service.process_data(test_data)
            
            assert result.success is True
            assert result.external_api_data is None
            assert "original_data" in result.processed_data
    
    def test_transform_data(self):
        """Тест трансформации данных"""
        service = DataProcessorService()
        
        test_data = {"key1": "value1", "key2": 123}
        result = service._transform_data(test_data)
        
        assert "original_data" in result
        assert result["original_data"] == test_data
        assert "processed_at" in result
        assert result["data_keys"] == ["key1", "key2"]
        assert result["data_type"] == "dict"
        assert result["transformation_applied"] is True
