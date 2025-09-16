"""
Pydantic модели для валидации данных
"""
from pydantic import BaseModel
from typing import Any, Dict, Optional
from datetime import datetime


class ProcessDataRequest(BaseModel):
    """Модель для входящих данных в POST /process_data/"""
    data: Dict[str, Any]


class ExternalApiResponse(BaseModel):
    """Модель ответа от внешнего API catfact.ninja"""
    fact: str
    length: int


class ProcessDataResponse(BaseModel):
    """Модель ответа для POST /process_data/"""
    success: bool
    message: str
    processed_data: Dict[str, Any]
    external_api_data: Optional[ExternalApiResponse] = None
    timestamp: datetime
    request_id: str


class ErrorResponse(BaseModel):
    """Модель для ошибок"""
    success: bool = False
    error: str
    detail: Optional[str] = None
    timestamp: datetime
    request_id: str


class HealthCheckResponse(BaseModel):
    """Модель для health check"""
    status: str
    app_name: str
    version: str
    timestamp: datetime
