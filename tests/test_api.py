"""
Unit тесты для API эндпоинтов
"""
import pytest
import httpx
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, patch
from datetime import datetime

from app.main import app
from app.models.schemas import ExternalApiResponse

client = TestClient(app)


class TestProcessDataEndpoint:
    """Тесты для POST /process_data/ эндпоинта"""
    
    @pytest.mark.asyncio
    async def test_process_data_success(self):
        """Тест успешной обработки данных"""
        # Мокаем внешний API
        mock_external_response = ExternalApiResponse(
            fact="Cats can rotate their ears 180 degrees.",
            length=42
        )
        
        with patch('app.services.external_api.ExternalApiService.get_cat_fact') as mock_get_fact, \
             patch('app.services.redis_service.RedisService.save_request') as mock_save:
            
            mock_get_fact.return_value = mock_external_response
            mock_save.return_value = True
            
            test_data = {"test_key": "test_value", "number": 123}
            
            response = client.post(
                "/api/v1/process_data/",
                json={"data": test_data}
            )
            
            assert response.status_code == 200
            data = response.json()
            
            assert data["success"] is True
            assert data["message"] == "Данные успешно обработаны"
            assert "processed_data" in data
            assert data["external_api_data"]["fact"] == "Cats can rotate their ears 180 degrees."
            assert data["external_api_data"]["length"] == 42
            assert "request_id" in data
            assert "timestamp" in data
    
    @pytest.mark.asyncio
    async def test_process_data_external_api_failure(self):
        """Тест обработки данных при недоступности внешнего API"""
        with patch('app.services.external_api.ExternalApiService.get_cat_fact') as mock_get_fact, \
             patch('app.services.redis_service.RedisService.save_request') as mock_save:
            
            mock_get_fact.return_value = None  # Внешний API недоступен
            mock_save.return_value = True
            
            test_data = {"test_key": "test_value"}
            
            response = client.post(
                "/api/v1/process_data/",
                json={"data": test_data}
            )
            
            assert response.status_code == 200
            data = response.json()
            
            assert data["success"] is True
            assert data["external_api_data"] is None
            assert "processed_data" in data
    
    def test_process_data_invalid_input(self):
        """Тест с некорректными входными данными"""
        response = client.post(
            "/api/v1/process_data/",
            json={"invalid_field": "test"}
        )
        
        assert response.status_code == 422  # Validation error


class TestHealthCheckEndpoint:
    """Тесты для GET /health/ эндпоинта"""
    
    @pytest.mark.asyncio
    async def test_health_check_healthy(self):
        """Тест health check при здоровом состоянии"""
        with patch('app.services.redis_service.RedisService.is_healthy') as mock_health:
            mock_health.return_value = True
            
            response = client.get("/api/v1/health/")
            
            assert response.status_code == 200
            data = response.json()
            
            assert data["status"] == "healthy"
            assert data["app_name"] == "Async Data Processing API"
            assert data["version"] == "1.0.0"
            assert "timestamp" in data
    
    @pytest.mark.asyncio
    async def test_health_check_degraded(self):
        """Тест health check при проблемах с Redis"""
        with patch('app.services.redis_service.RedisService.is_healthy') as mock_health:
            mock_health.return_value = False
            
            response = client.get("/api/v1/health/")
            
            assert response.status_code == 200
            data = response.json()
            
            assert data["status"] == "degraded"


class TestRootEndpoint:
    """Тесты для корневого эндпоинта"""
    
    def test_root_endpoint(self):
        """Тест корневого эндпоинта"""
        response = client.get("/api/v1/")
        
        assert response.status_code == 200
        data = response.json()
        
        assert "message" in data
        assert "version" in data
        assert "docs" in data
        assert "health" in data


class TestErrorHandling:
    """Тесты обработки ошибок"""
    
    def test_404_error(self):
        """Тест 404 ошибки"""
        response = client.get("/api/v1/nonexistent/")
        
        assert response.status_code == 404
    
    def test_method_not_allowed(self):
        """Тест ошибки метода не разрешен"""
        response = client.get("/api/v1/process_data/")
        
        assert response.status_code == 405
