"""
Конфигурация приложения через Pydantic BaseSettings
"""
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Настройки приложения"""
    
    # Основные настройки приложения
    app_name: str = "Async Data Processing API"
    app_version: str = "1.0.0"
    debug: bool = False
    
    # Настройки сервера
    host: str = "0.0.0.0"
    port: int = 8000
    
    # Настройки Redis
    redis_host: str = "localhost"
    redis_port: int = 6379
    redis_db: int = 0
    
    # Настройки внешнего API
    external_api_url: str = "https://catfact.ninja/fact"
    external_api_timeout: int = 10
    
    model_config = {
        "env_file": ".env",
        "case_sensitive": False
    }


# Глобальный экземпляр настроек
settings = Settings()
