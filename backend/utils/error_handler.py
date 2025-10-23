"""
Error handling utilities for English Assistant API
Provides standardized error handling and logging
"""
import logging
import traceback
from datetime import datetime
from typing import Any, Dict, Optional
from uuid import uuid4

from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse

from models.api_models import ErrorResponse


class ErrorHandler:
    """Centralized error handling for the application"""
    
    def __init__(self, logger_name: str = "english_assistant"):
        self.logger = logging.getLogger(logger_name)
    
    def handle_validation_error(
        self, 
        error: Exception, 
        request_id: Optional[str] = None
    ) -> ErrorResponse:
        """Handle Pydantic validation errors"""
        self.logger.warning(f"Validation error: {str(error)}")
        
        return ErrorResponse(
            error="validation_error",
            message="Invalid input data provided",
            details={"validation_errors": str(error)},
            request_id=request_id or str(uuid4())
        )
    
    def handle_model_error(
        self, 
        error: Exception, 
        model_name: str,
        request_id: Optional[str] = None
    ) -> ErrorResponse:
        """Handle AI model processing errors"""
        self.logger.error(f"Model error in {model_name}: {str(error)}")
        
        return ErrorResponse(
            error="model_error",
            message=f"Error processing request with {model_name}",
            details={
                "model": model_name,
                "error_type": type(error).__name__
            },
            request_id=request_id or str(uuid4())
        )
    
    def handle_database_error(
        self, 
        error: Exception,
        operation: str,
        request_id: Optional[str] = None
    ) -> ErrorResponse:
        """Handle database operation errors"""
        self.logger.error(f"Database error during {operation}: {str(error)}")
        
        return ErrorResponse(
            error="database_error",
            message="Database operation failed",
            details={
                "operation": operation,
                "error_type": type(error).__name__
            },
            request_id=request_id or str(uuid4())
        )
    
    def handle_not_found_error(
        self, 
        resource: str,
        resource_id: Optional[str] = None,
        request_id: Optional[str] = None
    ) -> ErrorResponse:
        """Handle resource not found errors"""
        message = f"{resource} not found"
        if resource_id:
            message += f" (ID: {resource_id})"
        
        self.logger.info(f"Resource not found: {message}")
        
        return ErrorResponse(
            error="not_found",
            message=message,
            details={
                "resource": resource,
                "resource_id": resource_id
            },
            request_id=request_id or str(uuid4())
        )
    
    def handle_rate_limit_error(
        self, 
        limit: int,
        window: str,
        request_id: Optional[str] = None
    ) -> ErrorResponse:
        """Handle rate limiting errors"""
        self.logger.warning(f"Rate limit exceeded: {limit} requests per {window}")
        
        return ErrorResponse(
            error="rate_limit_exceeded",
            message=f"Rate limit exceeded: {limit} requests per {window}",
            details={
                "limit": limit,
                "window": window,
                "retry_after": window
            },
            request_id=request_id or str(uuid4())
        )
    
    def handle_generic_error(
        self, 
        error: Exception,
        context: str = "Unknown operation",
        request_id: Optional[str] = None
    ) -> ErrorResponse:
        """Handle generic/unexpected errors"""
        self.logger.error(f"Unexpected error in {context}: {str(error)}")
        self.logger.debug(f"Traceback: {traceback.format_exc()}")
        
        return ErrorResponse(
            error="internal_error",
            message="An unexpected error occurred",
            details={
                "context": context,
                "error_type": type(error).__name__
            },
            request_id=request_id or str(uuid4())
        )


class HTTPExceptionHandler:
    """HTTP-specific exception handling for FastAPI"""
    
    @staticmethod
    def create_http_exception(
        status_code: int,
        error_response: ErrorResponse
    ) -> HTTPException:
        """Create HTTPException from ErrorResponse"""
        return HTTPException(
            status_code=status_code,
            detail=error_response.dict()
        )
    
    @staticmethod
    def validation_exception(message: str) -> HTTPException:
        """Create validation error HTTP exception"""
        return HTTPException(
            status_code=422,
            detail={
                "error": "validation_error",
                "message": message,
                "timestamp": datetime.now().isoformat()
            }
        )
    
    @staticmethod
    def not_found_exception(resource: str) -> HTTPException:
        """Create not found HTTP exception"""
        return HTTPException(
            status_code=404,
            detail={
                "error": "not_found",
                "message": f"{resource} not found",
                "timestamp": datetime.now().isoformat()
            }
        )
    
    @staticmethod
    def internal_server_exception(message: str = "Internal server error") -> HTTPException:
        """Create internal server error HTTP exception"""
        return HTTPException(
            status_code=500,
            detail={
                "error": "internal_error",
                "message": message,
                "timestamp": datetime.now().isoformat()
            }
        )


async def global_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Global exception handler for FastAPI application"""
    error_handler = ErrorHandler()
    request_id = str(uuid4())
    
    # Log the error with request details
    logger = logging.getLogger("english_assistant")
    logger.error(f"Unhandled exception in {request.method} {request.url}: {str(exc)}")
    logger.debug(f"Request ID: {request_id}, Traceback: {traceback.format_exc()}")
    
    # Create error response
    error_response = error_handler.handle_generic_error(
        exc, 
        context=f"{request.method} {request.url.path}",
        request_id=request_id
    )
    
    return JSONResponse(
        status_code=500,
        content=error_response.dict()
    )


class ModelErrorHandler:
    """Specialized error handling for AI model operations"""
    
    @staticmethod
    def handle_model_loading_error(model_name: str, error: Exception) -> ErrorResponse:
        """Handle errors during model loading"""
        return ErrorResponse(
            error="model_loading_error",
            message=f"Failed to load model: {model_name}",
            details={
                "model_name": model_name,
                "error_message": str(error),
                "suggestion": "Check model availability and cache directory"
            }
        )
    
    @staticmethod
    def handle_inference_error(model_name: str, error: Exception) -> ErrorResponse:
        """Handle errors during model inference"""
        return ErrorResponse(
            error="inference_error",
            message=f"Model inference failed: {model_name}",
            details={
                "model_name": model_name,
                "error_message": str(error),
                "suggestion": "Try with different input or check model status"
            }
        )
    
    @staticmethod
    def handle_timeout_error(model_name: str, timeout_seconds: int) -> ErrorResponse:
        """Handle model processing timeout errors"""
        return ErrorResponse(
            error="timeout_error",
            message=f"Model processing timeout: {model_name}",
            details={
                "model_name": model_name,
                "timeout_seconds": timeout_seconds,
                "suggestion": "Try with shorter input or increase timeout"
            }
        )