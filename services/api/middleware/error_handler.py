from fastapi import Request, status
from fastapi.responses import JSONResponse
import logging
from typing import Union, Dict, Any
import traceback

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class ErrorHandler:
    async def catch_exceptions_middleware(
        self,
        request: Request,
        call_next
    ) -> Union[JSONResponse, Any]:
        try:
            return await call_next(request)
        except Exception as e:
            return await self.handle_exception(request, e)

    async def handle_exception(
        self,
        request: Request,
        exc: Exception
    ) -> JSONResponse:
        error_id = self.log_error(request, exc)
        
        if hasattr(exc, 'status_code'):
            status_code = exc.status_code
        else:
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

        error_response = self.format_error_response(exc, error_id, status_code)
        
        return JSONResponse(
            status_code=status_code,
            content=error_response
        )

    def log_error(self, request: Request, exc: Exception) -> str:
        error_id = str(id(exc))
        
        error_details = {
            'error_id': error_id,
            'url': str(request.url),
            'method': request.method,
            'headers': dict(request.headers),
            'error_type': type(exc).__name__,
            'error_message': str(exc),
            'traceback': traceback.format_exc()
        }

        logger.error(
            f"Request failed: {error_details['error_type']}",
            extra=error_details
        )

        return error_id

    def format_error_response(
        self,
        exc: Exception,
        error_id: str,
        status_code: int
    ) -> Dict[str, Any]:
        error_type = type(exc).__name__
        
        # Custom error messages for known exceptions
        error_messages = {
            'ValidationError': 'Invalid input data',
            'AuthenticationError': 'Authentication failed',
            'PermissionError': 'Permission denied',
            'NotFoundError': 'Resource not found',
            'DatabaseError': 'Database operation failed',
            'RateLimitError': 'Rate limit exceeded',
            'ExternalAPIError': 'External service error'
        }

        return {
            'error': {
                'type': error_type,
                'message': error_messages.get(error_type, str(exc)),
                'id': error_id,
                'status': status_code,
                'details': self.get_error_details(exc)
            }
        }

    def get_error_details(self, exc: Exception) -> Dict[str, Any]:
        details = {}

        if hasattr(exc, 'detail'):
            details['detail'] = exc.detail
        
        if hasattr(exc, 'errors'):
            details['errors'] = exc.errors

        if hasattr(exc, 'code'):
            details['code'] = exc.code

        return details or None

# Custom exceptions
class ValidationError(Exception):
    def __init__(self, message: str, errors: Dict = None):
        super().__init__(message)
        self.status_code = status.HTTP_400_BAD_REQUEST
        self.errors = errors

class AuthenticationError(Exception):
    def __init__(self, message: str = "Authentication failed"):
        super().__init__(message)
        self.status_code = status.HTTP_401_UNAUTHORIZED

class PermissionError(Exception):
    def __init__(self, message: str = "Permission denied"):
        super().__init__(message)
        self.status_code = status.HTTP_403_FORBIDDEN

class NotFoundError(Exception):
    def __init__(self, message: str = "Resource not found"):
        super().__init__(message)
        self.status_code = status.HTTP_404_NOT_FOUND

class DatabaseError(Exception):
    def __init__(self, message: str = "Database operation failed"):
        super().__init__(message)
        self.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

class RateLimitError(Exception):
    def __init__(self, message: str = "Rate limit exceeded"):
        super().__init__(message)
        self.status_code = status.HTTP_429_TOO_MANY_REQUESTS

class ExternalAPIError(Exception):
    def __init__(self, message: str = "External service error"):
        super().__init__(message)
        self.status_code = status.HTTP_502_BAD_GATEWAY
