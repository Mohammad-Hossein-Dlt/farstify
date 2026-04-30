from faststream import ExceptionMiddleware
from src.infra.exceptions.exceptions import AppBaseException


exc_middleware = ExceptionMiddleware()
@exc_middleware.add_handler(Exception, publish=True)
def base_exc_handler(
    ex: Exception | AppBaseException,
) -> str:
        
    if isinstance(ex, AppBaseException):
        return ex.model_dump()
    
    return AppBaseException(500, "Internal server error").model_dump()